import React from 'react'

const FeatureBox = ({imageURL, heading, para}) => {
    return (
        <div className='flex flex-col text-center justify-center w-[30%] items-center p-8 rounded-2xl shadow-[0_0_30px_8px] shadow-slate-300'>
            <img src={`/assets/svgs/${imageURL}`} className='absolute mb-[22%] w-40' alt="" />
            <h2 className='text-2xl mt-[20%] text-slate-700'>{heading}</h2>
            <p className='text-md mt-2 text-slate-600'>{para}</p>
        </div>
    )
}

export default FeatureBox