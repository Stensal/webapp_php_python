
var path = require('path');
var targetDir = path.join(__dirname, "../../../../cppcms/static/portal");

module.exports = {
    entry: {
        'react': './react.jsx',
    },
    output: {
	path: path.join(targetDir, "shared"),
	filename: '[name].js'
    },
    // resolve: {
    // 	alias: {
    // 	    "react": "preact",
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
    }
};
