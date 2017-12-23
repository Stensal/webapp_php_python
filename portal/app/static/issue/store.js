/* -*- coding: utf-8 -*- */

import {observable, computed} from 'mobx';

class StoreBase {

    @observable loading = false;
    @observable err = "";
    @observable loaded = false;

    reset(){
	this.loading = false;
	this.err = '';
	this.loaded = false;
    }

}

class StoreConfig extends StoreBase{

    @observable config = {};
    @observable loaded = false;

    @computed get userValid(){
	return !!this.config.user.user_id;
    }

    load(){
	if(this.loading || this.loaded){ return; }
	this.loading = true;
	this.err = ''
	var url = '/issues/conf.json';
	fetch(url, {
	    method: 'POST',
	    credentials: 'include'
	}).then(function(r){
	    if(r.ok){
		return r.json();
	    }else{
		this.err = 'status: ' + r.status;
	    }
	}.bind(this)).then(function(r){
	    this.config = r;
	    this.loaded = true;
	    this.loading = false;
	}.bind(this)).catch(function(e){
	    this.err = e;
	    this.loading = false;
	}.bind(this));
    }

}

class StoreLabels extends StoreBase {

    @observable topLabels = [];
    // @observable loaded = false;

    load(){
	if(this.loading || this.loaded){ return; }
	this.loading = true;
	this.err = ''
	var url = '/issues/labels.json';
	fetch(url, {
	    method: 'POST',
	    credentials: 'include'
	}).then(function(r){
	    if(r.ok){
		return r.json();
	    }else{
		this.err = 'status: ' + r.status;
	    }
	}.bind(this)).then(function(r){
	    this.topLabels = r;
	    this.loaded = true;
	    this.loading = false;
	}.bind(this)).catch(function(e){
	    this.err = e;
	    this.loading = false;
	}.bind(this));
    }
    
}

class StoreNodeForm extends StoreBase {

    @observable content = {text: '', selection: null};
    @observable labelCnt = 0;
    @observable title = '';
    @observable invalid = {
	title: false,
	content: false
    };

    @observable success = false;

    _labelState = {};

    @computed get selectedLabels(){
	return this._labelState;
    }

    toggleLabel(labelId){
	if(this._labelState[labelId]){
	    this._labelState[labelId] = false;
	    this.labelCnt --;
	}else{
	    this._labelState[labelId] = true;
	    this.labelCnt ++;
	}
    }

    reset(){
	this.loading = false;
	this.err = '';
	this.invalid = {title: false, content: false};
	this.labelCnt = 0;
	this._labelState = {};
	this.title = '';
	this.content = {text: '', selection: null};
	this.success = false;
    }

    submit(){
	this.invalid = {title: false, content: false};
	this.success = false;
	var invalid = false;
	if(!this.title){
	    this.invalid.title = true;
	    invalid = true;
	}
	if(!this.content.text){
	    this.invalid.content = true;
	    invalid = true;
	}
	if(invalid){ return; }
	var url = '/issues/nodes/add.json';
	var form = new FormData();
	var labelsCsv = '';
	for(var labelId in this._labelState){
	    if(!this._labelState[labelId]){
		continue;
	    }
	    labelsCsv += labelsCsv ? ','+labelId : labelId;
	}
	form.set('content', this.content.text);
	form.set('title', this.title);
	form.set('labels', labelsCsv);
	form.set('parent_node_id', 0);
	form.set('issue_id', 0);
	fetch(url, {
	    method: 'POST',
	    credentials: 'include',
	    body: form
	}).then(function(r){
	    if(r.ok){
		return r.json();
	    }else{
		this.err = 'status: ' + r.status;
	    }
	}).then(function(r){
	    if(r.result){
		this.success = true;
	    }
	    this.loading = false;
	}.bind(this)).catch(function(e){
	    // this.reset();
	    if(e){ this.err = e };
	}.bind(this));
    }

}

class StoreNodes extends StoreBase {

    @observable nodes = [];
    @observable page = 1;
    @observable hasMore = false;
    @observable label = null;

    reset(){
	this.loading = false;
	this.err = '';
	this.nodes = [];
	this.page = 1;
	this.hasMore = false;
	this.label = null;
    }

    load(params){
	if(this.loading){ return; }
	this.loading = true;
	this.err = ''
	var url = '/issues/nodes.json';
	var form = new FormData();
	if(typeof params == 'object'){
	    for(var k in params){
		var v = params[k];
		if(v != null && typeof v != 'undefined'){
		    form.set(k, v);
		}
	    }
	}
	fetch(url, {
	    method: 'POST',
	    credentials: 'include',
	    body: form
	}).then(function(r){
	    if(r.ok){
		return r.json();
	    }else{
		this.err = 'status: ' + r.status;
	    }
	}).then(function(r){
	    this.nodes = r.nodes;
	    this.hasMore = r.has_more;
	    this.page = r.page;
	    this.label = r.label;
	    this.loading = false;
	}.bind(this)).catch(function(e){
	    this.reset();
	    if(e){ this.err = e };
	}.bind(this));
    }

}


class StoreIssue extends StoreBase{

    @observable nodes = [];

    reset(){
	super.reset();
	this.nodes = [];
    }

    load(issueId){
	console.info('load('+issueId+')');
	super.reset();
	this.loading = true;
	const url = '/issues/nodes/issue/' + issueId + '.json';
	fetch(url, {
	    method: 'POST',
	    credentials: 'include'
	}).then(function(r){
	    if(r.ok){
		return r.json();
	    }else{
		this.err = 'status: ' + r.status;
		this.loading = false;
	    }
	}).then(function(r){
	    this.nodes = r.nodes;
	    this.loading = false;
	    this.loaded = true;
	}.bind(this)).catch(function(e){
	    this.reset();
	    if(e){ this.err = e };
	}.bind(this));
    }

}


class StoreIssues extends StoreBase {

    conf = new StoreConfig();

    labels = new StoreLabels();

    list = new StoreNodes();

    form = new StoreNodeForm();

    issue = new StoreIssue();
}

export default StoreIssues;
