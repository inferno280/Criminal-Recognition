import React from 'react'

const Footer = () => {
    return (
        <footer className='w-full bg-gradient-to-l p-16 px-24 from-[#3641AF] to-[#7773D9] flex flex-col justify-center items-center'>
            <div className='flex items-center'>
                <img src="/assets/svgs/frLogo.png" className='h-20 w-20' alt="" />
                <h1 className='text-4xl mx-8 text-white font-["Viga"]'>TRACKFLIX</h1>
                <img src='/assets/policeLogo.png' className='h-20 w-20 rounded-lg' />
            </div>
            <div className='w-full flex justify-end items-center my-5'>
                <div className='flex flex-col text-slate-700 p-5 pt-6 justify-center w-[18%] rounded-tl-[50px] rounded-br-[50px] bg-[#bec3fd]'>
                    <span>Contact Us</span>
                    <span className='text-red-600'>trackflix@gmail.com</span>
                    <span>+91 9926685773</span>
                    <span className='w-2/3'>Bhilai institute of technolgy titurdhia,durg,chhattisgarh</span>
                </div>
            </div>
            <div className='flex w-full px-20 mt-5 items-center justify-between'>
                <div className='text-white'>
                    <span className='mx-2'>Privacy Policy</span>
                    <span className='mx-2'>Terms of use</span>
                </div>
                <div className='flex'>
                    <img src="/assets/svgs/instagram.png" className='h-10 w-10 mx-2' alt="" />
                    <img src="/assets/svgs/twitter.png" className='h-10 w-10 mx-2' alt="" />
                    <img src="/assets/svgs/facebook.png" className='h-10 w-10 mx-2' alt="" />
                </div>
            </div>
        </footer>
    )
}

export default Footer