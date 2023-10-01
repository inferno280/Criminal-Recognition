import React, { useState } from 'react'
import axios from 'axios';
import { useAuth0 } from "@auth0/auth0-react";
const Navbar = () => {
  const [enabled, setEnabled] = useState(false);
  const { user, isAuthenticated, isLoading, loginWithRedirect } = useAuth0();
  const handleClick = async () => {
    if (enabled) {
      setEnabled(false);
      const event = new KeyboardEvent('keydown', { key: 'esc' });
      event;
    }
    else {
      setEnabled(true);
      try {
        const response = await axios.get('http://localhost:5000/database-encode');
        console.log(response.data);
      } catch (error) {
        console.log(error);
      }
    }
  }
  console.log(user)
  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    element.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className='h-14 px-20 flex justify-between sticky top-0 items-center w-full z-50 bg-gradient-to-r from-[#9d9ffe] to-[#7a90fe]'>
      <img src="./assets/svgs/frLogo.png" className='h-10 bg-blue-400 text-blue-400 fill-blue-400' alt="" />
      <div className="font-['Viga'] flex items-center text-white">
        <button onClick={() => { scrollToSection('home') }} className='mx-4 transition-all duration-200 hover:text-red-600 font-inherit'>HOME</button>
        <button onClick={() => { scrollToSection('features') }} className='mx-4 transition-all duration-200 hover:text-red-600 font-inherit'>FEATURES</button>
        <button onClick={() => { scrollToSection('video') }} className='mx-4 transition-all duration-200 hover:text-red-600 font-inherit'>VFT</button>
        <button onClick={() => { scrollToSection('realtime') }} className='mx-4 transition-all duration-200 hover:text-red-600 font-inherit'>RFT</button>
        <button onClick={() => { scrollToSection('about') }} className='mx-4 transition-all duration-200 hover:text-red-600 font-inherit'>ABOUT US</button>
        <label onClick={handleClick} className={`cursor-pointer mx-4 transition-all duration-500 ${enabled ? "bg-[#6279ef]" : "bg-white"} p-[3px] flex rounded-full`}>
          <span className={`transition-all duration-500 ${enabled ? "translate-x-full bg-white" : "translate-x-0 bg-[#7a90fe]"} p-[0.55rem] rounded-full`} />
          <span className={`transition-all duration-500 ${enabled ? "-translate-x-full" : "translate-x-0"} p-[0.55rem] rounded-full`}></span>
        </label>
        <div>{user?.email}</div>
        <button onClick={() => loginWithRedirect()} className='hover:underline'>{isAuthenticated ? "LOGOUT" : "LOGIN"}</button>
      </div>
    </div>  
  )
}

export default Navbar