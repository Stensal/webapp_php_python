<?php

function get($key, $default=NULL) {
    return array_key_exists($key, $_GET) ? $_GET[$key] : $default;
}

class githubAuth{
    const OAUTH2_CLIENT_ID = '37235333098e7532b656';
    const OAUTH2_CLIENT_SECRET = 'afb0bd3e89a87fc060c5e4060954264d47656ab9';

    protected $authorizeURL = 'https://github.com/login/oauth/authorize';
    protected $tokenURL = 'https://github.com/login/oauth/access_token';
    protected $apiURLBase = 'https://api.github.com/';
    protected $homeUri = 'http://localhost:8000/auth.php';
    protected $redirectUri = 'http://localhost:8000/auth.php?callback';

    public function __construct(){
        session_start();

        if(get('act') == 'logout'){
            $this->authLogout();
            header('Location: ' . $this->homeUri);
            die();

        } else if(get('act') == 'login'){
            $this->authLogin();
        } else if(isset($_GET['callback'])){
            $this->authCallback();
        }
    }

    public function authLogin(){
        $_SESSION['state'] = hash('sha256', microtime(TRUE).rand().$_SERVER['REMOTE_ADDR']);

        unset($_SESSION['access_token']);

        $params = array(
            'client_id' => self::OAUTH2_CLIENT_ID,
            'redirect_uri' => $this->redirectUri,
            'scope' => 'user',
            'state' => $_SESSION['state']
        );

        // Redirect the user to Github's authorization page
        header('Location: ' . $this->authorizeURL . '?' . http_build_query($params));
        die();
    }

    public function authLogout(){
        unset($_SESSION['access_token']);
    }

    public function authCallback(){
        // Verify the state matches our stored state
        if(!get('state') || $_SESSION['state'] != get('state')) {
            header('Location: ' . $this->homeUri);
            die();
        }

        // Exchange the auth code for a token
        $token = $this->apiRequest($this->tokenURL, array(
            'client_id' => self::OAUTH2_CLIENT_ID,
            'client_secret' => self::OAUTH2_CLIENT_SECRET,
            'redirect_uri' => $this->redirectUri,
            'state' => $_SESSION['state'],
            'code' => get('code')
        ));
        $_SESSION['access_token'] = $token->access_token;

        header('Location: ' . $this->homeUri);
    }

    function apiRequest($url, $post=FALSE, $headers=array()) {
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
        curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)");

        if($post)
            curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($post));

        $headers[] = 'Accept: application/json';

        if($this->session('access_token'))
            $headers[] = 'Authorization: Bearer ' . $this->session('access_token');

        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

        $response = curl_exec($ch);

        return json_decode($response);
    }

    function session($key, $default=NULL) {
        return array_key_exists($key, $_SESSION) ? $_SESSION[$key] : $default;
    }

    function loggedIn(){
        if($this->session('access_token')){
            return true;
        }
        return false;
    }

    function userInfo(){
        return $this->apiRequest($this->apiURLBase . 'user');
    }
}

$auth = new githubAuth();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0">
    <title>Github login test</title>
    <meta name="keywords" content="keywords"/>
    <meta name="description" content="description"/>
    <style type="text/css">
        .login-box{font-family: Sans-serif;font-size: 24px;}
        .user-profile small{display: block; font-size: 14px;float: right;cursor: pointer;}
        .user-profile pre{background: #ccc;border-radius: 5px;padding: 10px;}
    </style>
</head>
<body>

<?php if($auth->loggedIn()): ?>
    <div class="user-profile">
        <h2>
            You are logged in with github
            <small><a href="?act=logout">logout</a></small>
        </h2>
        <h3>User Info</h3>
        <pre>
            <?php print_r($auth->userInfo()); ?>
        </pre>

        <h3>Session</h3>
        <pre>
            <?php print_r($_SESSION);?>
        </pre>
    </div>
<?php else: ?>
    <div class="login-box">
        <h3>You are not logged in</h3>
        <h2><a href="?act=login"><button type="button">github login</button></a></h2>
    </div>
<?php endif; ?>

</body>
</html>
