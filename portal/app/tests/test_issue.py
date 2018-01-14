import logging
import urllib.parse
import json
from tests.base import TestCaseBaseWithSession

from models.user import UserInfo, GithubUser
from models.issue import ISSUE_ST_PUBLISHED
from models.issue import ISSUE_NODE_TYPE_CONTENT
from models.issue import ISSUE_NODE_TYPE_LABELS
from models.helper import orm_session

from tests.mock_data import github_token, github_get_user_resp
from tests.mock_data import github_get_repos_resp
import users.views
import users.services
import issues.svc as svc


logger = logging.getLogger('tests')


class IssueTest(TestCaseBaseWithSession):

    def setUp(self):
        super(IssueTest, self).setUp()
        svc.add_default_labels()

    def test_label_ops(self):
        # svc._delete_all_labels()

        lb_text = 'a-test-label'
        lb = svc.add_label(lb_text)
        self.assertIsNotNone(lb)
        self.assertGreater(lb.label_id, 0)

        rs = svc.get_labels()
        self.assertIsNotNone(rs)

        svc.set_label_enabled(lb.label_id, 0)

    def test_labels_default(self):
        labels = svc.get_labels()
        self.assertGreater(len(labels), 0)
        lb = [lb for lb in labels if lb.label_text == 'bug']
        self.assertEqual(len(lb), 1)
        self.assertEqual(lb[0].label_text, 'bug')

    def test_labels_get_all(self):
        svc.add_default_labels()
        resp = self.client.get('/issues/labels.json')
        self.assertEqual(resp.status_code, 200)
        labels = json.loads(resp.data)
        self.assertTrue(isinstance(labels, list))
        self.assertGreater(len(labels), 0)

    def test_issue_get_nodes(self):
        resp = self.client.post('/issues/nodes.json',
                                data={
                                    'page': 1
                                })
        self.assertEqual(resp.status_code, 200)
        rs = json.loads(resp.data)
        self.assertTrue(isinstance(rs, dict))
        self.assertTrue('nodes' in rs \
                        and isinstance(rs['nodes'], list))
        self.assertTrue('has_more' in rs)
        self.assertTrue('page' in rs)
        self.assertTrue('page_size' in rs)

        nodes = rs['nodes']
        if len(nodes) > 0:
            node = nodes[0]
            self.assertTrue(isinstance(node, dict))
            self.assertGreater(node['node_id'], 0)

        resp = self.client.get('/issues/labels.json')
        labels = json.loads(resp.data)
        lb = [lb for lb in labels if lb['label_text'] == 'bug']
        label_id = lb[0]['label_id'] if lb else None
        if not label_id:
            logger.warning('label `bug` not found.')

        resp = self.client.post('/issues/nodes.json',
                                data={
                                    'page': 1,
                                    'label_id': label_id
                                })
        self.assertEqual(resp.status_code, 200)
        rs = json.loads(resp.data)
        self.assertTrue(isinstance(rs, dict))

    def test_issue_node_add(self):
        lb_bug = svc.get_label_by_text('bug')
        lb_help = svc.get_label_by_text('help wanted')
        label_ids = [lb_bug.label_id, lb_help.label_id]

        url = '/issues/nodes/add.json'
        form = {
            'node_type': ISSUE_NODE_TYPE_CONTENT,
            'parent_node_id': 0,
            'content': 'this is the content of an issue.',
            'status': ISSUE_ST_PUBLISHED,
            'labels': ','.join(map(str, label_ids))
        }
        resp = self.client.post(url, data=form)
        self.assertEqual(resp.status_code, 200)
        rs = json.loads(resp.data)
        self.assertTrue(isinstance(rs, dict) and 'node' in rs)
        node = rs['node']

        node_id = node['node_id']
        issue_id = node['issue_id']
        self.assertEqual(node_id, issue_id)

        # -- reply --
        form = {
            'node_type': ISSUE_NODE_TYPE_CONTENT,
            'issue_id': issue_id,
            'parent_node_id': node_id,
            'content': 'a reply.',
            'status': ISSUE_ST_PUBLISHED
        }
        resp = self.client.post(url, data=form)
        self.assertEqual(resp.status_code, 200)
        rs = json.loads(resp.data)
        self.assertTrue(isinstance(rs, dict) and 'node' in rs)
        node = rs['node']
        self.assertGreater(int(node['node_id']), 0)

        # -- update content --
        url = '/issues/nodes/node/%s/update_content.json' % node_id
        form = {
            'content': 'a reply. update something here...'
        }
        resp = self.client.post(url, data=form)
        self.assertEqual(resp.status_code, 200)
        rs = json.loads(resp.data)
        self.assertTrue(isinstance(rs, dict) and 'result' in rs)
        self.assertTrue(rs['result'])

        # -- set labels --
        url = '/issues/nodes/node/%s/set_labels.json' % node_id
        form = {
            'labels': ','.join(map(str, label_ids))
        }
        resp = self.client.post(url, data=form)
        self.assertEqual(resp.status_code, 200)
        rs = json.loads(resp.data)
        self.assertTrue(isinstance(rs, dict) and 'result' in rs)
        self.assertTrue('labels' in rs)
        self.assertTrue(rs['result'])
        _labels = rs['labels']
        _labels_idx = dict([(lb['label_id'], lb) for lb in _labels])
        for label_id in label_ids:
            self.assertTrue(label_id in _labels_idx)

        # -- get node --
        url = '/issues/nodes/issue/%s.json' % issue_id
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 200)
        rs = json.loads(resp.data)
        self.assertTrue(isinstance(rs, dict) and 'nodes' in rs)
        nodes = rs['nodes']
        self.assertGreater(len(nodes), 2)
        for node in nodes:
            if node['node_type'] == ISSUE_NODE_TYPE_LABELS:
                self.assertTrue('labels' in node)
                self.assertTrue(node['labels'] is not None)

    def test_markdown_convert_html(self):
        text = '# title'
        resp = self.client.post('/issues/md_to_html.json',
                                data={'text': text})
        rs = json.loads(resp.data)
        self.assertTrue(isinstance(rs, dict) and 'html' in rs)
        self.assertTrue(isinstance(rs['html'], str))
        self.assertTrue('<h1>' in rs['html'].lower())
