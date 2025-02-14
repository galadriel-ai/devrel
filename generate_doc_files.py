
if __name__ == "__main__":
    from gitingest import ingest

    summary, tree, content = ingest(source="https://github.com/galadriel-ai/galadriel",
                                    output="output_code.txt",
                                    exclude_patterns=["*.env", ".github/", "*.sh", "*.toml", "*.yml", "/tests", "/scripts", "/galadriel/docker"])
    print(summary)
    summary, tree, content = ingest(source="../docs/galadriel-network",
                                    output="output_docs.txt")
    print(summary)