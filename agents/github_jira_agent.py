import os
import tempfile
import shutil
from github import Github
from git import Repo
from atlassian import Jira
from langchain.agents import initialize_agent, Tool
from langchain.tools import BaseTool

# -------------------------------
# ✅ Configuration
# -------------------------------
from langchain_google_genai import ChatGoogleGenerativeAI
REPO_URL = "remote githubpath"
REPO_NAME = "user_name/repo_name"
from git import Repo

LOCAL_DIR = r"local repo path"

BRANCH_PREFIX = "auto-fix-"
GITHUB_TOKEN = "github_pat_xxx"

JIRA_URL = "https://xxx.atlassian.net"
JIRA_USER = "xxx"
JIRA_API_TOKEN = "api_token"
JIRA_PROJECT = "XXX"

TARGET_FILE_EXTENSIONS = [".py", ".js", ".css",".html"]  # files to consider

# -------------------------------
# ✅ Step 1: Jira – fetch tickets
# -------------------------------
jira = Jira(url=JIRA_URL, username=JIRA_USER, password=JIRA_API_TOKEN)
issues = jira.jql(f"project={JIRA_PROJECT} AND status != Done", limit=10)
jira_issues = issues.get("issues", [])
print(f"[INFO] Found {len(jira_issues)} Jira issues")

# -------------------------------
# ✅ Step 2: GitHub – setup repo
# -------------------------------
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)
default_branch = repo.default_branch
from pydantic import Field
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# clone or reuse local
if not os.path.exists(LOCAL_DIR):
    print("[INFO] Cloning repo...")
    Repo.clone_from(repo.clone_url.replace("https://", f"https://{GITHUB_TOKEN}@"), LOCAL_DIR, branch=default_branch)

local_repo = Repo(LOCAL_DIR)
print("✅ Repo loaded successfully:", local_repo.git_dir)
print("Current branch:", local_repo.active_branch)

class LocalFileModifyTool(BaseTool):
    name: str = "Local File Modify Tool"
    description: str = (
        "Given a file path and a Jira task description, reads the file, "
        "asks an LLM to apply modifications as per the task, "
        "and updates the file content with the LLM output."
    )

    project_root: str = Field(..., description="The local root directory of the repo.")
    llm: ChatGoogleGenerativeAI = Field(..., description="LLM instance to generate modifications.")

    def _run(self, file_path: str, jira_task_description: str) -> str:
        """Synchronously run the tool."""
        # Ensure file exists
        abs_path = os.path.join(self.project_root, file_path)
        if not os.path.exists(abs_path):
            return f"❌ File not found: {abs_path}"

        # Read current file content
        with open(abs_path, "r", encoding="utf-8") as f:
            current_code = f.read()

        # Build a prompt for LLM
        prompt_text = f"""
        You are an expert software engineer.
        Here is the file content that needs modification:  {current_code}
        Based on this Jira task:
        "{jira_task_description}"

        Modify the file content accordingly. Return ONLY the modified full file content, nothing else.
        """
        chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template("{input}")
        )
        modified_code = chain.run({"input": prompt_text})

        # Update the file
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(modified_code)

        return f"✅ File {file_path} modified successfully."

    async def _arun(self, file_path: str, jira_task_description: str) -> str:
        raise NotImplementedError("Async version not implemented.")

# -------------------------------
# ✅ LangChain – local file tool
# -------------------------------
class LocalFileSearchTool(BaseTool):
    name: str = "Local File Search Tool"
    description: str = "Searches files locally"

    def _run(self, query: str):
        matches = []
        for root, _, files in os.walk(LOCAL_DIR):
            for f in files:
                if any(f.endswith(ext) for ext in TARGET_FILE_EXTENSIONS):
                    path = os.path.join(root, f)
                    try:
                        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                            content = fh.read()
                            if query.lower() in content.lower():
                                matches.append(path)
                    except Exception as e:
                        continue
        return f"Found {len(matches)} relevant files: {matches}"

    async def _arun(self, query: str):
        raise NotImplementedError()

# LangChain agent
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", temperature=0.2)

tools = [LocalFileSearchTool(),LocalFileModifyTool()]
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# -------------------------------
# ✅ Step 3: Process each Jira issue
# -------------------------------
for issue in jira_issues:
    key = issue["key"]
    summary = issue["fields"]["summary"]
    print(f"\n🚀 Processing Jira {key}: {summary}")

    # Create branch
    branch_name = f"{BRANCH_PREFIX}{key.lower()}"
    try:
        # Check if branch exists
        repo.get_branch(branch_name)
        print(f"[INFO] Branch {branch_name} already exists.")
    except:
        print(f"[INFO] Creating branch {branch_name}")
        src = repo.get_branch(default_branch)
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=src.commit.sha)

    # Switch local repo to branch
    local_repo.git.fetch()
    try:
        local_repo.git.checkout(branch_name)
    except:
        local_repo.git.checkout('-b', branch_name, f'origin/{default_branch}')

    # Use agent to search files (can be extended to modify files)
    search_result = agent.run(f"Find files that might need changes for: {summary} and do the modification to each of the file")
    print("[DEBUG] Search Result:", search_result)

    # For demo, let's append a comment to a known file
    sample_file = os.path.join(LOCAL_DIR, "README.md")
    with open(sample_file, "a") as f:
        f.write(f"\n# Fix for {key}: {summary}\n")

    # Git commit & push
    local_repo.git.add(A=True)
    local_repo.index.commit(f"Fix for {key}: {summary}")
    local_repo.git.push("origin", branch_name)

    # Create PR
    pr = repo.create_pull(
        title=f"[AutoFix] {summary}",
        body=f"This PR addresses Jira issue {key}\n\n{summary}",
        head=branch_name,
        base=default_branch
    )
    print(f"✅ Created PR: {pr.html_url}")

print("🎉 Done processing all Jira issues.")
