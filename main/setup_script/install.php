<?php
/*
 * install.php
 *
 * Copyright (C) 2016 Erik Kalkoken
 *
 * Example script for installation a Slack app
 *
 * HISTORY
 * 18-NOV-2016 v1.1 Additional simplifications
 * 17-NOV-2016 v1.0 Initial based on installer script for evetools
 *
**/

// Referenced slack setup file from GitHub
// Added additional features to use OAuth 2.0 instead of the original OAuth 1.0

//////////// Functions

// Show consistent user message when installation process failed for any reason
// And allow restart of installation process
function showInstallFailed ($msg)
{
	$myScriptName = pathinfo (__FILE__, PATHINFO_BASENAME);
	
	echo '<p>' . $msg. '</p>';
	echo '<p>Installation failed - click <a href="' . $myScriptName. '">here</a> to start over</p>';	
}

//////////// Custom app parameters

// App Name
const APP_NAME = "Team Spirit";

// Slack OAuth parameter
// These are the basic parameters to identify your Slack app
// They can be found in the Slack app administration settings under "Basic Information"
$client_id = "5933772890579.5948056374419";
$client_secret = "8d1d5b9e81638194f42e8eba4daec9c4";

// Define scopes to be requested
// Here we request "commands" to be able to add our own slash commands 
// and "chat.write.user" which allows us to post messages on behalf of the installing user

// Currently the scopes are copy pasted from our current slack settings
$scope = "app_mentions:read,channels:history,channels:join,channels:read,chat:write,chat:write.customize,chat:write.public,commands,emoji:read,files:read,incoming-webhook,pins:read,users:read,users.profile:read,users:write,reminders:write";


//////////// Main

// Get filename of this script
$myScriptName = pathinfo (__FILE__, PATHINFO_BASENAME);

// Get value of URL parameters from request
// Will be NULL if parameter is not set
// Filter out tags and encode special characters
$input['code'] = filter_input (INPUT_GET, "code", FILTER_SANITIZE_STRING);
$input['state'] = filter_input (INPUT_GET, "state", FILTER_SANITIZE_STRING);
$input['error'] = filter_input (INPUT_GET, "error", FILTER_SANITIZE_STRING);

// Start output to browser

echo '
	<!DOCTYPE html>
	<html>
		<head>
		<title>Install ' . APP_NAME . '</title>
		</head>
	<body>
';
	
// Body

//////////////////////////////////////////////////////
// Page: Start-page
// This page is shown at the beginning
// It contains the "Add to Slack" button 
//////////////////////////////////////////////////////

if ( ($input['code'] === null) && ($input['error'] === null) )
{	
	$slack_call = "https://slack.com/oauth/authorize";
	$slack_call .= "?scope=$scope";
	$slack_call .= "&client_id=$client_id";
	
	echo '
		<h1>Installing ' . APP_NAME . ' for your Slack team</h1>
		
		<p>Please click the "Add to Slack" button below to start the installation process. You will then be routed to Slack and asked to log into the Slack team you want to add this app to.</p>
		
		<p>Please complete the login process and authorize this app for your Slack team when asked. You will be routed back to this site when the installation process is complete. Depending on the configuration of your Slack team you may need admin or owner role to add this app.</p>
		<p>Note that you can always delete this app later from your Slack team if you don\'t want to use it any longer.</p>
		<p style="font-weight:bold;">!! Please click the button below to start the installation process !!</p>
		<p><a href="' . $slack_call . '">
		<img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a></p>
		<br>
	';
}

//////////////////////////////////////////////////////
// Page: Processing of access code from Slack 
// Slack has called this script with the code parameter which contains the access code
//////////////////////////////////////////////////////

elseif ( $input['code'] !== null )
{
	// we will now exchange the received access code into a full access token_get_all
	// by calling Slack once again
	
	// get the full URI to the current script
	$redirect_uri ='https://';
	$redirect_uri .= $_SERVER['HTTP_HOST'] . dirname($_SERVER['REQUEST_URI']);
	$redirect_uri .= "/". $myScriptName;

	// Build the request url for starting the oauth process

	// Update from original script, changed from oauth v1 to v2, Slack updated this
	$url = "https://slack.com/api/oauth.v2.access?client_id=$client_id";
	$url .= "&client_secret=$client_secret&code=" . $input['code'] . "&redirect_uri=$redirect_uri";
	
	$ch = curl_init($url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 2);
		
	$result = curl_exec($ch);
	$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
	
	if ( $result === false || ($http_code != '200') )
	{
		// the curl request failed
		$curlerror = curl_error($ch);
		$msg = "Error while trying to access the slack API - Curl error: '$curlerror' - http error: '$http_code'";
		showInstallFailed ($msg);
	}
	else
	{
		$response = json_decode($result, true);
		
		// Check if json_decode suceeded
		if ($response === null) 
		{
			$msg = "Auth process could not be completed successfully. Response from Slack was: '$response'";
			showInstallFailed ($msg);
		}
		// Check if Slack returned OK for the auth process
		elseif ($response['ok'] === false)
		{
			$errorMsg = isset ($response['error']) ? $response['error'] : "no error message";
			$msg = "Auth process could not be completed successfully. Response from Slack was: '$errorMsg'";
			showInstallFailed ($msg);
		}
		else
		{
			// Installation process has suceeded
			
			// $response contains the access token, information about the Slack team
			// additional information based on the requested scope
			
			// here is an example for how the response will look:
			//
			//	{
			//		"access_token": "xoxp-XXXXXXXX-XXXXXXXX-XXXXX",
			//		"scope": "incoming-webhook,commands,bot",
			//		"team_name": "Team Installing Your Hook",
			//		"team_id": "XXXXXXXXXX",
			//		"incoming_webhook": {
			//			"url": "https://hooks.slack.com/TXXXXX/BXXXXX/XXXXXXXXXX",
			//			"channel": "#channel-it-will-post-to",
			//			"configuration_url": "https://teamname.slack.com/services/BXXXXX"
			//		},
			//		"bot":{
			//			"bot_user_id":"UTTTTTTTTTTR",
			//			"bot_access_token":"xoxb-XXXXXXXXXXXX-TTTTTTTTTTTTTT"
			//		}
			//	}
			
			
			// Add some code here to further process and store the received tokens and information from Slack
					
			$teamName = $response['team_name'];
			echo '
				<h2>Installation completed successfully.</h2>
				<p>Thank you for installing ' . APP_NAME . ' to your Slack team ' . $teamName. '</p>
				<p>You can now close this browser window and return to Slack to try out the new app.</p>
			';
		}
	}
}

//////////////////////////////////////////////////////
// Page: Processing of errors returned from Slack (Hidden)
//////////////////////////////////////////////////////

elseif ( $input['error'] !== null )
{
	$msg = "Received an error from Slack: '" . $input['error'] . "'";
	showInstallFailed ($msg);
}

?>