import yaml


class MetaMarkdown:
    def __init__(self):
        self.metadata = {}
        self.content = ""

    @property
    def metadatas(self):
        return (
            "---\n"
            + yaml.safe_dump(self.metadata, sort_keys=False, default_flow_style=None)
            + "---\n"
        )

    @classmethod
    def load(cls, file_obj):
        metadata = ""
        in_metadata = False
        content = ""
        for line in file_obj.read().split("\n"):
            if line == "---":
                metadata.append(line)
                in_metadata = not in_metadata
            elif in_metadata:
                metadata += line + "\n"
            else:
                content += line + "\n"
        obj = MetaMarkdown()
        obj.metadata = yaml.safe_load(metadata)
        obj.content = content.rstrip()
        return obj

    @classmethod
    def loads(cls, string):
        metadata = ""
        in_metadata = False
        content = ""
        for line in string.split("\n"):
            if line == "---":
                in_metadata = not in_metadata
            elif in_metadata:
                metadata += line + "\n"
            else:
                content += line + "\n"
        obj = MetaMarkdown()
        obj.metadata = yaml.safe_load(metadata)
        obj.content = content.rstrip()
        return obj

    def dumps(self, default_flow_style=None):
        metadata = yaml.dump(
            self.metadata, sort_keys=False, default_flow_style=default_flow_style
        )
        return "---\n" + metadata + "---\n" + self.content
