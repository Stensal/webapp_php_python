/* -*- coding: utf-8 -*- */

import {observer} from 'mobx-react';
import IssueNode from './issue-node.jsx';

@observer
class IssueNodeList extends React.Component{

    render(){
	const {store} = this.props;
	var {loading, err} = store.list;
	var {nodes, page, hasMore, label} = store.list;
	nodes = nodes.slice();
	// nodes.push({})
	return (<div className="pure-u-1">
		<ul className="issues-list">

		{nodes.length <= 0
		 ? (<div>no issues.</div>)
		 : (<div></div>)}
		
		{nodes.map((node, i) => {
		    return (<IssueNode 
			    store={store} 
			    node={node} 
			    key={i}/>);
		})}
		
		</ul>
		</div>);
    }
}

export default IssueNodeList;
