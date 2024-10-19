import pytest
import zipfile
import io
from commands import CommandDispatcher

# Фикстура для создания тестового zip-архива
@pytest.fixture
def vfs_zip():
    # Создание файловой структуры внутри zip-архива
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('folder1/file1.txt', 'File 1 content')
        zf.writestr('folder1/file2.txt', 'File 2 content')
        zf.writestr('folder2/file3.txt', 'File 3 content')
        zf.writestr('folder2/subfolder/file4.txt', 'File 4 content')
    data.seek(0)
    return data

# Тест для команды ls
def test_ls(vfs_zip):
    dispatcher = CommandDispatcher(vfs_zip)
    
    result = dispatcher.execute('ls')
    assert result == "folder1\nfolder2", f"Expected 'folder1\\nfolder2', but got {result}"

    # Переходим в folder1 и выполняем команду ls
    dispatcher.execute('cd folder1')
    result = dispatcher.execute('ls')
    assert result == "file1.txt\nfile2.txt", f"Expected 'file1.txt\\nfile2.txt', but got {result}"

# Тест для команды cd
def test_cd(vfs_zip):
    dispatcher = CommandDispatcher(vfs_zip)

    # Переход в folder1
    result = dispatcher.execute('cd folder1')
    assert dispatcher.current_path == "/folder1/", f"Expected path '/folder1/', but got {dispatcher.current_path}"

    # Переход в subfolder (не существующую папку)
    result = dispatcher.execute('cd subfolder')
    assert result == "Error: path not found", "Expected error message for invalid path"

    # Возврат в корневую директорию
    dispatcher.execute('cd ..')
    assert dispatcher.current_path == "/", f"Expected path '/', but got {dispatcher.current_path}"

# Тест для команды pwd
def test_pwd(vfs_zip):
    dispatcher = CommandDispatcher(vfs_zip)

    # Проверка начальной директории
    result = dispatcher.execute('pwd')
    assert result == "/", f"Expected path '/', but got {result}"

    # Переход в folder2/subfolder и проверка pwd
    dispatcher.execute('cd folder2')
    dispatcher.execute('cd subfolder')
    result = dispatcher.execute('pwd')
    assert result == "/folder2/subfolder/", f"Expected path '/folder2/subfolder/', but got {result}"

# Тест для команды exit
def test_exit(vfs_zip):
    dispatcher = CommandDispatcher(vfs_zip)

    # Выполняем команду exit
    result = dispatcher.execute('exit')
    assert result == "exit", f"Expected 'exit', but got {result}"

