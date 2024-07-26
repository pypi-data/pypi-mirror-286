def is_running_on_colab():
    try:
        import google.colab  # NOQA

        return True
    except ImportError:
        return False


def sanitaize_path(path: str) -> bool:
    if path.startswith(".") or path.startswith("/"):
        return False
    return True


def generate_colab_IF(port: int):
    return f"""
  <script>var colab_server_port={port}</script>
  <script>var colab_server=1</script>
  <script defer="defer" src="http://localhost:{port}/front/index.js"></script>
  <div id="app" style="width:100%;height:100%"></div>
  """


def start_colab_IF(port: int):
    from IPython.display import HTML

    html = generate_colab_IF(port)
    return HTML(html)
