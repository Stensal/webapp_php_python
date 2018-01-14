/* -*- coding: utf-8 -*- */

import {observer} from 'mobx-react';
import {AniLoading} from '../shared/widgets.jsx';


@observer
class IssuePage extends React.Component{

    componentDidMount(){
	const {store, match} = this.props;
	const issueId = match.params.issue_id;
	if(!issueId || !store){ return; }
	store.issue.load(issueId);
    }

    thread(){
	const {store, match} = this.props;
	var {nodes} = store.issue;
	nodes = nodes.slice();
	return (<div>
		thread nodes..
		</div>);
    }

    render(){
	const {store, match} = this.props;
	const {loading, err, loaded} = store.issue;
	return (<div className="container">
		issue_id: {match.params.issue_id}
		
		<div>
		{loading
		 ? (<AniLoading/>)
		 : (loaded
		    ? (this.thread())
		    : (<span className=''>
		       ...
		       </span>))}
		</div>

		<div>
		{err ? (<span 
			className='alert alert-danger'>{err}</span>): null}
		</div>

		</div>);
    }

}

export default IssuePage;
