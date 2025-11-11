import json
from dagger import function, object_type, Secret

@object_type
class GitLab:
    @function
    def get_merge_request_id(
        self,
        token: Secret,
        server: str,
        project_id: str,
        merge_request_title: str,
    ) -> str:
        mrs_json = self.list_merge_requests(server, token, project_id)

        try:
            mrs = json.loads(mrs_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse merge requests JSON: {e}") from e

        for mr in mrs:
            if mr.get("title") == merge_request_title:
                return str(mr["iid"])

        raise ValueError(f"Merge request {merge_request_title!r} not found")
