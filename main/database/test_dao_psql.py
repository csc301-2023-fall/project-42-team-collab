from datetime import datetime

import pytest

from database.dao_psql import DAOPostgreSQL


class TestDAOPostgreSQL:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.dao = DAOPostgreSQL()
        conn = self.dao.get_connection()
        cursor = conn.cursor()
        print('Set up')
        cursor.execute('DROP SCHEMA IF EXISTS t0001 CASCADE;')
        yield

    def test_create_workspace(self):
        try:
            result = self.dao.create_workspace('t0001')
            assert result is True
        except Exception as e:
            pytest.fail(f"Unexpected error: {e}")

    def test_add_user(self):
        try:
            self.dao.create_workspace('t0001')
            result = self.dao.add_user('t0001', 'test_slack_id', 'test_name')
            assert result is True
        except Exception as e:
            pytest.fail(f"Unexpected error: {e}")

    def test_delete_user(self):
        try:
            self.dao.create_workspace('t0001')
            result = self.dao.delete_user('t0001', 'test_slack_id')
            assert result is True
        except Exception as e:
            pytest.fail(f"Unexpected error: {e}")

    def test_add_channel(self):
        try:
            self.dao.create_workspace('t0001')
            result = self.dao.add_channel('t0001', 'test_channel_id',
                                          'test_name')
            assert result is True
        except Exception as e:
            pytest.fail(f"Unexpected error: {e}")

    def test_delete_channel(self):
        try:
            self.dao.create_workspace('t0001')
            result = self.dao.delete_channel('t0001', 'test_channel_id')
            assert result is True
        except Exception as e:
            pytest.fail(f"Unexpected error: {e}")

    def test_add_message(self):
        try:
            self.dao.create_workspace('t0001')
            time = datetime.now()
            self.dao.add_channel('t0001', 'test_channel_id', 'test_name')
            self.dao.add_user('t0001', 'test_from_slack_id', 'Jiawei')
            self.dao.add_user('t0001', 'test_to_slack_id', 'Scott')
            self.dao.add_corp_values('t0001', ['value1'])
            result = self.dao.add_message('t0001', 'test_channel_id',
                                          'test_msg_id', time,
                                          'test_from_slack_id',
                                          'test_to_slack_id', 'test_text',
                                          ['value1'])
            assert result is True
        except Exception as e:
            pytest.fail(f"Unexpected error: {e}")

    def test_add_corp_values(self):
        try:
            self.dao.create_workspace('t0001')
            result = self.dao.add_corp_values('t0001', ['value1', 'value2'])
            assert result is True
        except Exception as e:
            pytest.fail(f"Unexpected error: {e}")

    def test_delete_corp_values(self):
        try:
            self.dao.create_workspace('t0001')
            result = self.dao.delete_corp_values('t0001', ['value1', 'value2'])
            assert result is True
        except Exception as e:
            pytest.fail(f"Unexpected error: {e}")

    def test_get_corp_values(self):
        try:
            self.dao.create_workspace('t0001')
            values = self.dao.get_corp_values('t0001')
            assert isinstance(values, list)
            assert len(values) == 0
            self.dao.add_corp_values('t0001', ['value1', 'value2'])
            values = self.dao.get_corp_values('t0001')
            assert len(values) == 2
        except Exception as e:
            pytest.fail(f"Unexpected error: {e}")


if __name__ == '__main__':
    pytest.main()
