import React from 'react';
import Navbar from '../components/Navbar';
import FeatureBox from '../components/FeatureBox';
import FaceTracking from '../components/FaceTracking';
import About from '../components/About';
import Footer from '../components/Footer';
import Model from '../components/Model';
import Background from '../components/Background';
import axios from 'axios';
const Home = () => {
  const para1 = "Our video/webcam face tracking technology utilizes advanced facial recognition algorithms to accurately detect and identify individuals. This feature enables law enforcement agencies and security professionals to match faces against databases of known criminals, aiding in the swift identification and apprehension of suspects."
  const para2 = "With our real-time tracking and alert system, our video/webcam face tracking technology provides immediate notifications when a person of interest is detected. This feature allows security personnel to respond rapidly and take proactive measures to prevent crimes or intervene in time-critical situations."
  const para3 = "We understand the importance of privacy, and our video/webcam face tracking technology is designed with robust privacy protection measures. Facial data is securely stored, and access is strictly controlled, ensuring compliance with privacy regulations and safeguarding sensitive information."

  const handleClick = async () => {
    const res = await axios.get('http://localhost:5000/media-pipe');
    console.log(res.data);
  }

  return (
    <section className='min-h-screen flex flex-col'>
      <Navbar />
      <section>
        <Background id="home" />
        <section className='flex w-full mt-36 h-1/3 px-10 justify-evenly'>
          <Model id="video" imageUrl="videoCamera.svg" modelPara="Enhancing Safety through Advanced Technology" modelHeading="Unleash the Power of Video Face Tracking in Criminal Detection" modelName="VIDEO FACE TRACKING" />
          <Model id="realtime" imageUrl="faceCamera.svg" modelPara="Enhancing Security through Real-Time Insights" modelHeading="Empowering Crime Detection with Real-time Face Tracking" modelName="REALTIME FACE TRACKING" />
          <Model id="database" imageUrl="database.svg" modelPara="Unleashing the Potential of Video Face Tracking" modelHeading="Powerful Database for Criminal Detection" modelName="DATABASE STORAGE" />
        </section>
        <section id="features" className='w-full my-24 flex flex-col justify-center items-center'>
          <h1 className='text-5xl font-["Viga"] text-slate-700'>FEATURES</h1>
          <aside className='flex mt-[10%] w-full px-16 justify-evenly'>
            <FeatureBox heading="Accurate Facial Recognition" imageURL="Ellipse 1.svg" para={para1} />
            <FeatureBox heading="Real-Time Tracking and Alerts" imageURL="Ellipse 2.svg" para={para2} />
            <FeatureBox heading="Privacy Protection" imageURL="Ellipse 3.svg" para={para3} />
          </aside>
        </section>
        <section className='w-full'>
          <FaceTracking id="video" name="VIDEO FACE TRACKING" />
          <FaceTracking id="realtime" name="REALTIME FACE TRACKING" />
          <FaceTracking id="database" name="DATABASE STORAGE" />
        </section>
        <About id="about" />
        <button className='bg-blue-500 rounded ml-[50%] my-10 p-2 px-3 text-white' onClick={handleClick}>Media Pipe</button>
      </section>
      <Footer />
    </section>
  )
}

export default Home
