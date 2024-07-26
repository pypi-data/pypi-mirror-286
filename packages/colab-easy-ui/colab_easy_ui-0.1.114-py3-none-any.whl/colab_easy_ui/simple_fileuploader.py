import fire
from colab_easy_ui.ColabEasyUI import ColabEasyUI
import logging
import os


logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("multipart").setLevel(logging.WARNING)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)


def run_server(
    ipython=None,
    logfile=None,
    port: int | None = None,
    allow_origins: list[str] = ["*"],
    upload_dir: str = "upload",
    file_title: str | None = None,
    file_name: str | None = None,
    # display=None,
    # download_func=None,
):
    c = ColabEasyUI.get_instance(port=port, allow_origins=allow_origins)
    port = c.port
    # ファイルアップローダ
    assert file_title is not None and file_name is not None
    c.enable_file_uploader(upload_dir, {file_title: file_name})

    # 静的ファイルのマウント
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    static_files_path = os.path.join(current_dir, "frontend_fileuploader/dist")
    c.mount_static_folder("/front", static_files_path)

    # サーバー起動
    port = c.start()
    print(f"[debug] open http://localhost:{port}/front")
    return port


def wrapped_run_server(
    ipython=None,
    logfile=None,
    port: int | None = None,
    allow_origins: list[str] = ["*"],
    upload_dir: str = "upload",
    file_title: str | None = None,
    file_name: str | None = None,
):
    """
    run_serverの戻り値であるportを標準出力に出さないようにするためのラッパ。
    """
    run_server(
        ipython,
        logfile,
        port=port,
        allow_origins=allow_origins,
        upload_dir=upload_dir,
        file_title=file_title,
        file_name=file_name,
    )


def main():
    fire.Fire(wrapped_run_server)
