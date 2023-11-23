from __init__ import *
from datetime import datetime

if __name__ == '__main__':
    DAO = get_DAO()

    # DAO.create_workspace('ml')
    # values = DAO.get_corp_values('ml')
    # DAO.add_user('ml', '001', 'Jiawei')
    # DAO.add_user('ml', '002', 'Ray')
    # DAO.add_channel('ml', 'ABC', 'dbpart')
    result = DAO.add_channel('t0001', 'test_channel_id',
                                  'test_name')
    DAO.add_message(workspace_id='ml', channel_id='ABC', channel_name='dbpart',
                    msg_id='N5', time=datetime.now(), from_slack_id='001', to_slack_id='002',
                    from_username='Jiawei', to_username='Ray', text='gjnc',
                    kudos_value=['Leadership', 'srt', 'sdsd', 'Innovation'])

