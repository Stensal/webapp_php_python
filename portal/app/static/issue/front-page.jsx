/* -*- coding: utf-8 -*- */

import {observer} from 'mobx-react';
import LabelsBar from './labels-bar.jsx';
import IssueNodeList from './issue-node-list.jsx';


@observer
class FrontPage extends React.Component{

    componentDidMount(){
	this.load();
    }

    componentWillReceiveProps(newProps){
	this.load();
    }

    load(){
	const {store, match} = this.props;
	var q = {};
	if(match.params.page){
	    q.page = match.params.page;
	}
	if(match.params.label){
	    q.label_id = match.params.label;
	}
	console.info(q);
	store.list.load(q);
    }
    
    render(){
	const {match, store} = this.props;
	return (<div className='issue-front-page'>
		<LabelsBar store={store} match={match}/>
		
		<div className="container pure-g">
		<IssueNodeList {...this.props}/>
		</div>

		</div>);
    }

}


export default FrontPage;
