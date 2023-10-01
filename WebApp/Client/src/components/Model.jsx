import React from 'react'

const Model = ({id, imageUrl, modelPara, modelHeading, modelName}) => {
    const scrollToSection = (id)=>{
        const element = document.getElementById(id);
        element.scrollIntoView({behavior: 'smooth'});
    }
    return (
        <aside className={`flex flex-col justify-center w-[30%]`}>
            <h2 className='text-3xl font-["Viga"] text-slate-600'>{modelName}</h2>
            <div className={`flex relative bottom-2`}>
                <div className={`flex flex-col items-start justify-center w-40% py-6`}>
                    <h3 className='text-lg text-slate-700'>{modelHeading}</h3>
                    <p className="text-sm text-slate-600 my-2 w-[70%]">{modelPara}</p>
                    <button onClick={()=>{scrollToSection(id)}} className='py-2 px-4 rounded mt-2 bg-[#4A57EB] text-white'>Try Now</button>
                </div>
                <img src={`/assets/svgs/${imageUrl}`} className='w-[40%] relative right-10' alt="" />
            </div>
        </aside>
    )
}

export default Model