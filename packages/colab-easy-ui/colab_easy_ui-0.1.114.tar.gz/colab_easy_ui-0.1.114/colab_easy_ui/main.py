import fire
from colab_easy_ui.ColabEasyUI import ColabEasyUI, JsonApiFunc

import functools
from colab_easy_ui.plugins.download_function.Downloader import DownloadParams
from colab_easy_ui.plugins.download_function.download_function import download
from colab_easy_ui.plugins.extract_feats_function import extract_feats
from colab_easy_ui.plugins.generate_filelist_function import generate_filelist
from colab_easy_ui.plugins.get_server_info_function import get_server_info_function
from colab_easy_ui.plugins.onnx_download_function import onnx_download

from colab_easy_ui.plugins.preprocess_function import preprocess
from colab_easy_ui.plugins.train_function import train
from colab_easy_ui.plugins.onnx_export_function import onnx_export

from colab_easy_ui.plugins.unzip_function import unzip
import logging
import os

downloadParams = [
    DownloadParams(
        display_name="whisper_tiny.pt",
        url="https://openaipublic.azureedge.net/main/whisper/models/65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9/tiny.pt",
        saveTo="./models/embedder/whisper_tiny.pt",
        hash="65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9",
    ),
    DownloadParams(
        display_name="amitaro-nof0-e0100-s010500.pt",
        url="https://huggingface.co/wok000/vcclient_model/resolve/main/easy-vc/amitaro-nof0-e0100-s010500.pt",
        saveTo="./models/pretrained/easy-vc/amitaro-nof0-e0100-s010500.pt",
        hash="b749d9dfaef1a93871a83f7e9f7d318071aafe823fc8da50a937d5eb5928983a",
    ),
]


logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("multipart").setLevel(logging.WARNING)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)


def run_server(
    ipython=None,
    logfile=None,
    port: int | None = None,
    allow_origins: list[str] = ["*"],
    # display=None,
    # download_func=None,
):
    c = ColabEasyUI.get_instance(port=port, allow_origins=allow_origins)
    port = c.port
    # ファイルアップローダ
    c.enable_file_uploader("upload", {"Voice(zip)": "voice.zip"})

    # Tensorboardの登録
    c.enable_colab_internal_fetcher("trainer", ipython, logfile)

    # 機能登録
    c.register_functions(
        [
            # backgroundタスクのパラレル化がむずいので、一つずつ別タスクにする（TOBE IMPROVED）。
            JsonApiFunc(
                id="download_whisper",
                type="progress",
                display_name="whisper",
                method="GET",
                path="/download1",
                func=functools.partial(download, port=port, downloadParams=downloadParams[0:1]),
            ),
            JsonApiFunc(
                id="download_pretrain",
                type="progress",
                display_name="pretrain",
                method="GET",
                path="/download2",
                func=functools.partial(download, port=port, downloadParams=downloadParams[1:2]),
            ),
            JsonApiFunc(
                id="unzip",
                type="progress",
                display_name="unzip",
                method="GET",
                path="/unzip",
                func=functools.partial(unzip, port=port, zip_path="upload/voice.zip", extract_to="raw_data"),
            ),
            JsonApiFunc(
                id="preprocess",
                type="progress",
                display_name="preprocess",
                method="GET",
                path="/preprocess",
                func=functools.partial(
                    preprocess,
                    port=port,
                ),
            ),
            JsonApiFunc(
                id="extract_feats",
                type="progress",
                display_name="extract feats",
                method="GET",
                path="/feats",
                func=functools.partial(
                    extract_feats,
                    port=port,
                ),
            ),
            JsonApiFunc(
                id="generate_filelist",
                type="progress",
                display_name="generate filelist",
                method="GET",
                path="/filelist",
                func=functools.partial(
                    generate_filelist,
                    port=port,
                ),
            ),
            JsonApiFunc(
                id="start_train",
                type="progress",
                display_name="start train",
                method="GET",
                path="/train",
                func=functools.partial(
                    train,
                    port=port,
                ),
            ),
            JsonApiFunc(
                id="onnx_export",
                type="progress",
                display_name="onnx export",
                method="GET",
                path="/onnx_export",
                func=functools.partial(
                    onnx_export,
                    port=port,
                ),
            ),
            JsonApiFunc(
                id="get_server_info",
                type="get",
                display_name="get_server_info",
                method="GET",
                path="/get_server_info",
                func=functools.partial(get_server_info_function, dataset_folder="raw_data", project_folder="trainer"),
            ),
            JsonApiFunc(
                id="onnx_download",
                type="download",
                display_name="onnx_download",
                method="GET",
                path="/onnx_download",
                func=functools.partial(onnx_download),
            ),
        ]
    )

    # 静的ファイルのマウント
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    static_files_path = os.path.join(current_dir, "frontend/dist")
    c.mount_static_folder("/front", static_files_path)

    # サーバー起動
    port = c.start()
    print(f"open http://localhost:{port}/front")
    return port


def wrapped_run_server(
    ipython=None,
    logfile=None,
    port: int | None = None,
    allow_origins: list[str] = ["*"],
):
    """
    run_serverの戻り値であるportを標準出力に出さないようにするためのラッパ。
    """
    run_server(ipython, logfile, port=port, allow_origins=allow_origins)


def main():
    fire.Fire(wrapped_run_server)
