/* -*- coding: utf-8 -*- */

import {observer} from 'mobx-react';
import StoreUser from './store.js';

@observer
class SyncLink extends React.Component {

    render(){
	var {store} = this.props;
	return (<span>
		<a href="javascript:;"
		className="pure-menu-link"
		onClick={() => { store.sync.syncAll(); }}>
		{store.sync.loading 
		 ? (<span>loading...</span>)
		 : (<span>
		    Sync
		    {store.sync.err
		     ? (<span className='err'>!</span>)
		     : null}
		    </span>)}
		</a>
		</span>);
    }

}


var store = new StoreUser();
var span = document.getElementById('linkSync')
ReactDOM.render(<SyncLink store={store}/>, span)
