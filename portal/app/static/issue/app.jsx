/* -*- coding: utf-8 -*- */

import {observer} from 'mobx-react';
import StoreIssues from './store.js';
import {
    BrowserRouter, // as Router,
    HashRouter,
    Route,
    Switch
} from 'react-router-dom';

import {AniLoading} from '../shared/widgets.jsx';

import '../shared/widgets.css';
import './issue.css';

import FrontPage from './front-page.jsx';
import IssueForm from './issue-form.jsx';
import IssuePage from './issue-page.jsx';


const APP_MOUNT_POINT = "/issues/app";


class IssuesApp extends React.Component{

    render(){
	const {store} = this.props;
	return (<HashRouter>
		<Switch>
		
		<Route path="/new"
		component={(m) => <IssueForm {...m} store={store}/>}/>

		<Route path="/issue/:issue_id"
		component={(m) => <IssuePage {...m} store={store}/>} />

		<Route path="/label/:label/page/:page"
		component={(m) => <FrontPage {...m} store={store}/>} />
		<Route path="/label/:label"
		component={(m) => {
		    return (<FrontPage {...m} store={store} 
			    labelId={m.match.params.label}/>);
		}} />
		<Route path="/page/:page"
		component={(m) => <FrontPage {...m} store={store}/>} />
		<Route path="/"
		component={(m) => <FrontPage {...m} store={store}/>} />
		
		</Switch>
		</HashRouter>);
    }

}

@observer
class Loader extends React.Component{

    componentDidMount(){
	// todo: load some configuration data here...
	const {store} = this.props;
	store.conf.load();
    }

    render(){
	const {store} = this.props;
	if(store.conf.loading){
	    return (<div className='container'>
		    <AniLoading/>
		    </div>);
	}else if(!store.conf.loaded){
	    if(store.conf.err){
		return (<div className='err'>{store.conf.err}</div>);
	    }else{
		return (<div></div>);
	    }
	}
	return (<IssuesApp {...this.props}/>);
    }

}

const store = new StoreIssues();
ReactDOM.render(<Loader store={store}/>, 
		document.getElementById('issues-app'));
