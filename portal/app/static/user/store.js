/* -*- coding: utf-8 -*- */

import {observable} from 'mobx';

class StoreUserSync{

    @observable loading = false;
    @observable err = "";

    @observable success = false;

    syncAll(){
	if(this.loading){ return; }
	this.loading = true;
	this.err = ''
	var url = '/users/github/sync_all.json';
	fetch(url, {
	    method: 'POST',
	    credentials: 'include'
	}).then(function(r){
	    if(r.ok){
		return r.json();
	    }else{
		this.err = 'status: ' + r.status;
	    }
	}).then(function(r){
	    this.loading = false;
	}.bind(this)).catch(function(e){
	    this.err = e;
	    this.loading = false;
	}.bind(this));
    }

}

class StoreUser {
    
    sync = new StoreUserSync();

}

export default StoreUser;
