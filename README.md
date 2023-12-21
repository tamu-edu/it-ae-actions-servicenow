# it-ae-actions-servicenow

This composite action is used to modify a Service Now request

## Example usages

- Add a comment
```yaml
steps:
  - name: Update Service Now Request
    uses: tamu-edu/it-ae-actions-servicenow@v1.0
    with:
      sn-base-url: ${{ vars.SN_BASE_URL }}
      sn-username: ${{ secrets.SN_USERNAME }}
      sn-password: ${{ secrets.SN_PASSWORD }}
      action-version: v1.0
      sn-request-id: 99e15216db4fb114c02e6909139619d2
      sn-action: add_comment
      sn-input1: My comment
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

- Add a work note
```yaml
steps:
  - name: Update Service Now Request
    uses: tamu-edu/it-ae-actions-servicenow@v1.0
    with:
      sn-base-url: ${{ vars.SN_BASE_URL }}
      sn-username: ${{ secrets.SN_USERNAME }}
      sn-password: ${{ secrets.SN_PASSWORD }}
      action-version: v1.0
      sn-request-id: 99e15216db4fb114c02e6909139619d2
      sn-action: add_work_notes
      sn-input1: My work note
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

- Close a Request
```yaml
steps:
  - name: Update Service Now Request
    uses: tamu-edu/it-ae-actions-servicenow@v1.0
    with:
      sn-base-url: ${{ vars.SN_BASE_URL }}
      sn-username: ${{ secrets.SN_USERNAME }}
      sn-password: ${{ secrets.SN_PASSWORD }}
      action-version: v1.0
      sn-request-id: 99e15216db4fb114c02e6909139619d2
      sn-action: close_request
      sn-input1: ""
      github-token: ${{ secrets.GITHUB_TOKEN }}
```

- Update a Request variable called 'resource_url':
```yaml
steps:
  - name: Update Service Now Request
    uses: tamu-edu/it-ae-actions-servicenow@v1.0
    with:
      sn-base-url: ${{ vars.SN_BASE_URL }}
      sn-username: ${{ secrets.SN_USERNAME }}
      sn-password: ${{ secrets.SN_PASSWORD }}
      action-version: v1.0
      sn-request-id: 99e15216db4fb114c02e6909139619d2
      sn-action: update_request_variable
      sn-input1: resource_url
      sn-input2: Testing composite action 2
      github-token: ${{ secrets.GITHUB_TOKEN }}
```