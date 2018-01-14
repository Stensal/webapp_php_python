/* -*- coding: utf-8 -*- */

import {observer} from 'mobx-react';
import {
    Router,
    Redirect,
    Link
} from 'react-router-dom';
import ReactMde, {ReactMdeCommands} from 'react-mde';

import 'react-mde/lib/styles/css/react-mde-all.css';


@observer
class IssueDraftOptions extends React.Component{

    componentDidMount(){
	const {store} = this.props;
	store.labels.load();
    }

    render(){
	const {store} = this.props;
	var topLabels = store.labels.topLabels.slice();
	var cnt = store.form.labelCnt;
	return (<div className='draft-options'>
		<div className="dropdown show">
		<a className="btn btn-lg btn-secondary dropdown-toggle" 
		href="javascript:;" role="button" data-toggle="dropdown" 
		aria-haspopup="true" aria-expanded="false">
		Labels
		{cnt > 0 ? (<span><i> </i>
			    (<i className='fa fa-check'/> 
			     {cnt})
			    </span>) : null}
		</a>
		<div className="dropdown-menu" 
		aria-labelledby="dropdownMenuLink">
		{[topLabels, cnt][0].map((label, i) => {
		    var active = store.form.selectedLabels[label.label_id];
		    return (<a href="javascript:;" 
			    key={i} 
			    className={active 
				       ? "dropdown-item active"
				       : "dropdown-item"}
			    onClick={(e) => {
				e.stopPropagation();
				e.preventDefault();
				store.form.toggleLabel(label.label_id)
			    }}>
			    {label.label_text}
			    <i> </i>
			    {active
			     ? (<i className='fa fa-check'/>)
			     : (<i/>)}
			    </a>);
		})}
		</div>
		</div>
		</div>);
    }

}

@observer
class IssueForm extends React.Component{

    componentDidMount(){
	const {store} = this.props;
	store.form.reset();
    }

    form(){
	const {store} = this.props;
	const invalid = store.form.invalid;
	const userValid = !!store.conf.config.user.user_id;
	return (<div>

		<div className='form-group'>
		{/*<label htmlFor="issue-title">Title:</label>*/}
		<input type="text" placeholder="Title" required
		className={invalid.title ? 'form-control is-invalid' : 'form-control'} 
		id="issue-title"
		onChange={(e) => { store.form.title = e.target.value; }}
		value={store.form.title} maxLength={120}/>
		{invalid.title
		 ? (<div className='invalid-feedback'>
		    Please provide a title for the issue.
		    </div>)
		 : (<div className='form-text text-muted'></div>)}
		</div>
		
		<div className='form-group'>
		<ReactMde value={store.form.content} id="issue-content"
		textAreaProps={{
		    className: invalid.content ? 'form-control is-invalid' : 'form-control',
		    placeholder: 'Leave a comment'
		}}
		commands={ReactMdeCommands.getDefaultCommands()}
		onChange={(value) => {
		    store.form.content = value;
		}} />
		{/*{invalid.content
		 ? (<div className='invalid-feedback'>
		    Issue requires description or comment.
		    </div>)
		 : null}*/}
		</div>

		<div className='form-group'>
		<div className='container'>
		<div className='row'>
		<div className='col-auto mr-auto'></div>
		<div className='col-auto'>
		{store.form.loading
		 ? (<button className='btn btn-secondary' disabled>
		    <i className='fa fa-hourglass-half'></i>
		    </button>)
		 : (<button 
		    className={userValid 
			       ? "btn btn-primary"
			       : "btn btn-secondary"}
		    disabled={!userValid}
		    onClick={() => { store.form.submit(); }}>
		    Submit issue</button>)}
		</div>
		</div>
		</div>
		</div>

		</div>);
    }

    render(){
	var {store} = this.props;
	const {userValid} = store.conf;
	return (<div className='container issue-form'>
		<h2>New issue</h2>

		<div className='pure-g'>
		<div className='pure-u-2-3'>
		{store.form.success
		 ? (<Router {...this.props}>
		    <Redirect from="/new" to="/"/>
		    </Router>)
		 : this.form()}
		</div>

		<div className='pure-u-1-3 form-options'>
		{store.conf.config.is_admin
		 ? (<IssueDraftOptions store={store}/>)
		 : (<div>
		    {userValid
		     ? (<div></div>)
		     : (<div>
			<button className='btn btn-info'
			onClick={() => {location.href = '/users/signup';}}>
			Sign in to post an issue
			</button>
			</div>)}
		    </div>)}
		</div>

		</div>

		</div>);
    }

}

export default IssueForm;
