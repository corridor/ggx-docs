# CI CD Integrations

There are scenarios when approval of an object is not confined to the reviewers registered on the platform.
The client may have an external application, where other stakeholders are already onboarded and would want to
review objects on the platform.
Corridor provides the ability to interact with such 3rd party applications, using API calls, and integrating their review.
This can be accomplished by defining a custom handler that uses the base approval handler class exposed by Corridor.

## Handler class

The user would need to define a `CustomApprovalHandler` which would inherit Corridor's base approval handler class:
`corridor_api.config.handlers.ApprovalHandler`

The logic for approval would be defined by the following method(s) inside `CustomApprovalHandler`.

- `send_action(review, action)`
- `receive_action(review_id, payload)`

## Example

The example focuses on a model, which needs to be sent for review.
We can configure what information we want to send to the tool (in `send_action`).
The tool will expose an endpoint that would take that information, create a model entry on their side,
carry out the necessary approval process, and send the feedback to us (in `receive_action`).
`reviewId` is the key and would be used for communications.

```python
from corridor_api.config.handlers import ApprovalHandler


class CustomApprovalHandler(ApprovalHandler):
 name = 'external_tool'

    def send_action(self, review, action):
        '''
 :param review: review_object
 :param action: Action taken by the user on the platform for the given review
 - 'Request Approval'
 - 'Resubmit'
 - 'Cancel'
 - 'Remind'
 - 'Edit' (if the object is in the 'Pending Approval' state and it is edited)
 '''
 url = 'http://externaltool.example.com/cp_review/'  # assuming the 3rd party app is running on PORT: 7006
 review_id = review.id
 object_ = review.object  # `corridor` object

        from corridor import Model

        # if we need to restrict the 3rd party approvals to Models only
        if not isinstance(object_, Model):
            raise NotImplementedError(f'{type(object_)} is not expected to be used with "{self.name}" tool!!!')

 json_info = {
            'modelId': object_.parent_id,
            'modelName': object_.name,
            'modelVersion': object_.version,
            'modelVersionId': object_.id,
            'modelGroup': object_.group,
            'createdBy': object_.created_by,
            'reviewId': review_id,
            'responsibilityId': review.responsibility.id,
            'responsibilityName': review.responsibility.name,
            'action': action,
            'comment': review.comment,
 }
 headers = {}  # any headers can be configured (optional)
 res = requests.post(url + str(review_id), json=json_info, headers=headers)
        return {'status': res.status_code}

    def receive_action(self, review_id, payload):
        '''
 :param review_id:  id corresponding to the review object
 (this is the same id that was sent by CP when requesting the review)
 :param payload:    payload expects 2 kwargs
 - 'action': one of 'Accept'/'Need Info'/'Need Changes'/'Reject'/'Comment'
 - 'comment': any comment which the external_tool's reviewer makes
 :return:           dictionary with `action` and `comment` for the review with id: `review_id`
 '''
        # The external app needs to do a POST call with `action` and `comment` as part of the payload.
        # the endpoint would look like below (assuming corridor-api is running on port 5000):
        #   `http://localhost:5000/api/v1/models/review/<<reviewId>>/external`
 action = payload.get('action')
 comment = payload.get('comment')

        # do some processing, if required
 comment = 'No comment' if comment is None else comment

        return {'action': action, 'comment': comment}

```

## Configurations

Approval handler-related configurations need to be set in `api_config.py` along with other configurations.
(assuming the `CustomApprovalHandler` class is defined in the file `custom_approval_handler.py`).

```python
THIRD_PARTY_APPROVALS = {
    'external_tool': {
        'handler': 'custom_approval_handler.CustomApprovalHandler',
 },
}
```
