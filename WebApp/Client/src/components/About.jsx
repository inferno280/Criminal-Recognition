import React from 'react'

const About = ({id}) => {
    return (
        <section id={id} className='my-20 flex flex-col items-center justify-center px-[20%]'>
            <h1 className='text-4xl text-slate-700 my-5 font-["Viga"]'>ABOUT US</h1>
            <p className='text-xl text-slate-600 my-2 text-center'>
                At TrackFlix, we are at the forefront of leveraging video and webcam face tracking technology for the vital task of criminal detection. Our mission is to empower law enforcement agencies and security professionals with innovative solutions that enhance their capabilities in identifying and apprehending criminals. With our advanced video and webcam face tracking technology, we are revolutionizing the way crimes are detected and communities are kept safe.
            </p>
            <p className='text-xl text-slate-600 my-2 text-center'>
                We understand the critical importance of accuracy, speed, and privacy in criminal detection efforts. That's why our cutting-edge technology combines state-of-the-art computer vision algorithms, facial recognition, and real-time analytics to deliver exceptional results. By harnessing the power of video and webcam face tracking, we provide law enforcement agencies with the tools they need to extract valuable information from surveillance footage, match faces against databases, and identify suspects with unparalleled precision.
            </p>
        </section>
    )
}

export default About   