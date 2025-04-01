import requests
import json

# GitHub Personal Access Token과 리포지토리 정보 설정
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN_HERE"  # 발급받은 토큰으로 변경
OWNER = "spring-projects"               # 리포지토리 소유자 (예: "octocat")
REPO = "spring-framework"                 # 리포지토리 이름 (예: "Hello-World")

# API 호출 시 필요한 헤더 설정
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

# 1. 리포지토리 파일 목록 추출 함수
def fetch_repo_contents(owner, repo, path=""):
    """
    지정한 경로(path)의 파일 및 디렉토리 목록을 가져오는 함수
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()  # 파일 또는 디렉토리 목록 반환
    else:
        print(f"Error fetching contents at {path}: {response.status_code}")
        return None

# 재귀적으로 파일 목록을 가져오는 함수 (디렉토리 내부 탐색)
def recursive_fetch_files(owner, repo, path=""):
    """
    리포지토리 내 모든 파일의 경로를 재귀적으로 가져오는 함수
    """
    files = []
    contents = fetch_repo_contents(owner, repo, path)
    if contents is None:
        return files

    for item in contents:
        if item["type"] == "file":
            files.append(item["path"])
        elif item["type"] == "dir":
            files.extend(recursive_fetch_files(owner, repo, item["path"]))
    return files

# 2. 이슈 데이터 추출 함수
def fetch_issues(owner, repo, state="all"):
    """
    해당 리포지토리의 이슈를 페이지 단위로 모두 가져오는 함수
    (풀 리퀘스트는 제외)
    """
    issues = []
    page = 1
    per_page = 100  # 최대 100개씩 가져올 수 있음
    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        params = {
            "state": state,
            "per_page": per_page,
            "page": page
        }
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"Error fetching issues: {response.status_code}")
            break
        data = response.json()
        # 풀 리퀘스트도 포함될 수 있으므로, 'pull_request' 키가 없는 항목만 이슈로 취급
        data = [issue for issue in data if "pull_request" not in issue]
        if not data:
            break
        issues.extend(data)
        page += 1
    return issues

# 3. 풀 리퀘스트(Pull Request) 데이터 추출 함수
def fetch_pull_requests(owner, repo, state="all"):
    """
    해당 리포지토리의 풀 리퀘스트를 페이지 단위로 모두 가져오는 함수
    """
    pulls = []
    page = 1
    per_page = 100
    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
        params = {
            "state": state,
            "per_page": per_page,
            "page": page
        }
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"Error fetching pull requests: {response.status_code}")
            break
        data = response.json()
        if not data:
            break
        pulls.extend(data)
        page += 1
    return pulls

# 4. 메인 함수: 모든 데이터를 추출하고 JSON 파일로 저장
def main():
    # 리포지토리 파일 경로 추출
    print("리포지토리 파일 목록 추출 중...")
    repo_files = recursive_fetch_files(OWNER, REPO)
    print(f"총 파일 수: {len(repo_files)}")
    with open("repo_files.json", "w", encoding="utf-8") as f:
        json.dump(repo_files, f, ensure_ascii=False, indent=2)

    # 이슈 데이터 추출
    print("이슈 데이터 추출 중...")
    issues = fetch_issues(OWNER, REPO)
    print(f"총 이슈 수: {len(issues)}")
    with open("issues.json", "w", encoding="utf-8") as f:
        json.dump(issues, f, ensure_ascii=False, indent=2)

    # 풀 리퀘스트 데이터 추출
    print("풀 리퀘스트 데이터 추출 중...")
    pulls = fetch_pull_requests(OWNER, REPO)
    print(f"총 풀 리퀘스트 수: {len(pulls)}")
    with open("pull_requests.json", "w", encoding="utf-8") as f:
        json.dump(pulls, f, ensure_ascii=False, indent=2)

    print("모든 데이터 추출 및 저장 완료!")

if __name__ == "__main__":
    main()
