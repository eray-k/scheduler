from src.database.models.user import User, UserPublicWithActivities
from src.database.models.activity import Activity

User.update_forward_refs(Activity=Activity)
UserPublicWithActivities.update_forward_refs(Activity=Activity)
Activity.update_forward_refs(User=User)
