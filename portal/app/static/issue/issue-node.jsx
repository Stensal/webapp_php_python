/* -*- coding: utf-8 -*- */

import {Link} from 'react-router-dom';


class IssueNode extends React.Component{

    componentDidMount(){
	// --
    }

    render(){
	var {node} = this.props;
	const avatarUrl = "/users/user/"+ node.created_user_id +"/avatar.png";
	const createdAt = new Date(node.created_at);
	return (<li className="issues-item issues-sec">

		<p className="issues-author">
		<a href="#">
		<img src={avatarUrl} alt="avatar" className="avatar img-circle img-responsive"/>
		<span className="author">{node.created_user_name}</span>
		</a>
		<span className="date">{moment(createdAt).fromNow()}</span>
		</p>

		<h4 className="h4 title">
		<span className="label">labels</span>
		<Link to={"/issue/" + node.issue_id}
			  className="title-text">{node.title}</Link>
		</h4>
		</li>);
    }

}

export default IssueNode;
