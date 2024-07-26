class WorkspaceHeader:
    def render(self, project_name):
        return (
            f"Workspace {project_name}".ljust(50)
            + " " * 13
            + "[CONTEXT LOADED]\n"
            + "=" * 79
        )
