import React from 'react'

const Background = ({id}) => {
    return (
        <section id={id} className='w-full h-[550px] relative flex flex-col justify-center items-start'>
            <h1 className='font-["Viga"] ml-[10%] z-[1] text-6xl my-2 text-white'>WELCOME TO</h1>
            <h1 className='font-["Viga"] ml-[10%] z-[1] text-6xl my-2 text-white p-3 rounded bg-[#4A51ED]'>TRACKFLIX</h1>
            <img src="/assets/svgs/homeBg.svg" className='absolute h-full w-full object-cover' alt="" />
            <img src="/assets/svgs/character.svg" className='absolute bottom-0 h-full w-full object-contain z-10' alt="" />
        </section>
    )
}

export default Background