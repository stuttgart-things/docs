```python
gitlab = dag.gitlab()
id = gitlab.get_merge_request_id(token, server, project_id, merge_request_title)
```

```ts
const gitlab = dag.gitlab();
const id = await gitlab.getMergeRequestId(token, server, projectId, mergeRequestTitle);
```

```go
gitlab := dag.Gitlab()
id, err := gitlab.GetMergeRequestId(token, server, projectID, mergeRequestTitle)
```
