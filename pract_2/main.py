import git

import tempfile
import shutil# функции для работы с файловой системой
import argparse#парсинга аргументов командной строки
import subprocess#внешних команд и программ из Python

def clone_repo(repo_url):#  клонирует Git-репозиторий по заданному URL
    temp_dir = tempfile.mkdtemp()
    print(f"Cloning repository from {repo_url}...")
    repo = git.Repo.clone_from(repo_url, temp_dir)
    print("Repository cloned successfully.")
    return repo, temp_dir # возвращает объект репозитория и путь к временной директории

def get_commits_for_tag(repo, tag_name):# получает список всех коммитов, связанных с заданным тегом в репозитории
    tagged_commit = repo.tags[tag_name].commit
    commits = list(repo.iter_commits(tagged_commit))
    return commits

def get_files_in_commit(commit):#возвращает список файлов, измененных в заданном коммите
    files = commit.stats.files.keys()
    return files

def build_dependency_graph(commits):#создаем словарь, где ключами являются SHA-хеши коммитов
    #а значениями - списки файлов, измененных в этих коммитах
    graph = {}
    for commit in commits:
        files = get_files_in_commit(commit)
        graph[commit.hexsha] = files
    return graph

def generate_mermaid_graph(graph):
    lines = ["graph TD"]
    for commit, files in graph.items():
        node_name = f"commit_{commit[:7]}"
        file_list = "<br/>".join(files)
        lines.append(f"{node_name} -->|{file_list}| {node_name}_files")
    return "\n".join(lines)

def save_graph_as_mmd(mermaid_graph, mmd_path):
    with open(mmd_path, 'w') as f:
        f.write(mermaid_graph)

def convert_mmd_to_png(mmd_path, png_path):
    subprocess.run(['mmdc', '-i', mmd_path, '-o', png_path, '-s', '100'], check=True)
    print(f"Graph converted to PNG: {png_path}")


def main():
    # Парсим аргументы командной строки
    parser = argparse.ArgumentParser(description="Create a Mermaid graph of git dependencies.")
    parser.add_argument('--repo', type=str, required=True, help="URL to the GitHub repository.")
    parser.add_argument('--mmd', type=str, required=True, help="Path to the output MMD file.")
    parser.add_argument('--tag', type=str, required=True, help="Tag name in the repository.")
    parser.add_argument('--out', type=str, required=True, help="Path to the output PNG file.")

    args = parser.parse_args()
    
    # Клонируем репозиторий
    repo, temp_dir = clone_repo(args.repo)
    try:
        # Получаем список коммитов для заданного тега
        commits = get_commits_for_tag(repo, args.tag)
        graph = build_dependency_graph(commits)
        mermaid_graph = generate_mermaid_graph(graph)
        save_graph_as_mmd(mermaid_graph, args.mmd)
        convert_mmd_to_png(args.mmd, args.out)
    finally:
        shutil.rmtree(temp_dir)

    print("Graph saved successfully as a PNG file!")

if __name__ == "__main__":
    main()