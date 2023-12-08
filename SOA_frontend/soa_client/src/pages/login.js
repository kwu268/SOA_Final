import '../App.css';
import { useState } from 'react';
import { freeUser, nazim } from "./userList";


function Login() {
	const [userLogin, setUserLogin] = useState({
		username: "",
		password: "",
	});
	
	function handleUsernameUpdate(e) {
		setUserLogin({
			...userLogin,
			username: e.target.value
		});
	}

	function handlePasswordUpdate(e) {
		setUserLogin({
			...userLogin,
			password: e.target.value
		});
	}
	
	const handleLoginAttempt = (e) => {
		
		if (userLogin.username === freeUser.username && userLogin.password === freeUser.password) {
			localStorage.setItem("login",true)
			localStorage.setItem("premium",false)
			
		} else if (userLogin.username === nazim.username && userLogin.password === nazim.password) {
			localStorage.setItem("login",true)
			localStorage.setItem("premium",true)
		}
		
	}
	return(
		<div className='wrapper'>
			<form onSubmit={handleLoginAttempt} className='wrapper'>
				<label>
					Username: 
					<input
						className='search-input'
						value = {userLogin.username}
						onChange = {handleUsernameUpdate}
					/>
				</label>
				<label>
					Password: 
					<input
						className='search-input'
						value = {userLogin.password}
						onChange = {handlePasswordUpdate}
					/>
				</label>
				<button className="custom-button"type="submit">Login</button>
			</form>
		</div>
	);
}

export default Login;