
var path = require('path');
var targetDir = path.join(__dirname, "../../../../cppcms/static/portal");

module.exports = {
    entry: {
        'app': './app.jsx',
    },
    output: {
	path: path.join(targetDir, "issue"),
	filename: '[name].js'
    },
    // resolve: {
    // 	alias: {
    // 	    "react": "preact-compat",
    // 	    "react-dom": "preact-compat"
    // 	}
    // },
    module: {
	loaders: [{
	    test: /\.js[x]?$/i, 
 	    loader: 'babel-loader',
	    exclude: /node_modules/
        }, {
	    test: /\.css$/i,
	    loaders: ['style-loader', 'css-loader']
	}]
    },
    externals: {
	'react': 'React',
	'react-dom': 'ReactDOM'
    }
};
