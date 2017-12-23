/* -*- coding: utf-8 -*- */

import {observer} from 'mobx-react';
import {
    BrowserRouter, // as Router,
    Route,
    Switch,
    Link
} from 'react-router-dom';


const LabelLink = (props) => {
    return (<li className='label-item'>
	    <Route path={props.to} children={({match}) => {
		var cls = match ? 'label-link current' : 'label-link';
		return (<Link to={match ? '/' : props.to} 
			className={cls}>
			{props.label.label_text}</Link>);
	    }}/>
	    </li>);
};

@observer
class LabelsBar extends React.Component {

    componentDidMount(){
	const {store} = this.props;
	if(!store){ return; }
	store.labels.load();
    }
    
    get labelId(){
	return this.props.match.params.label;
    }

    render(){
	const {match, store} = this.props;
	var topLabels = store ? store.labels.topLabels.slice() : [];
	// console.info(topLabels);
	return (<div className="container">
		<section className="pure-g issues-labels">
		<div className="pure-u-1 issues-labels-inner clearfix container">
		<ul className="label-list list-inline pull-left">

		{topLabels.map((label, i) => {
		    return (<LabelLink label={label} key={i} 
			    to={"/label/" + label.label_id}
			    match={match}/>);
		})}
		</ul>
		<div className="pull-right issues-edit">
		<Link to="/new" className="edit-link pull-right">
		<i className="fa fa-pencil"></i>
		</Link>
		<form action="./" className="search-box pull-right">
		<a href="#" className="search-icon">
		<i className="fa fa-search"></i>
		</a>
		<input type="text" className="search-input" placeholder="Search Issues"/>
		</form>
		<div className="clear"></div>
		
		</div>
		<span id="tab-collapse">Category <i className="fa fa-caret-down"></i></span>
		</div>
		</section>
		</div>);
    }

}

export default LabelsBar;
