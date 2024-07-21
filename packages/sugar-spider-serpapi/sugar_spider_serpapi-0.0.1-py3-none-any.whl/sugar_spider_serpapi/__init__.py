from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("sugar_spider_serpapi")
except PackageNotFoundError:
    # package is not installed
    pass
