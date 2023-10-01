import React, { useEffect, useState } from 'react'
import axios from 'axios';
import './scroll.css';
import io from 'socket.io-client';

const socket = io('http://127.0.0.1:5000');

const FaceTracking = ({ name, id }) => {

    const [file1, setFile1] = useState(null);
    const [file2, setFile2] = useState(null);
    const [timestamps, setTimestamps] = useState([]);
    const [frames, setFrames] = useState([]);

    const storeImage = async (urlName) => {
        const formData = new FormData();
        formData.append('image', file1);
        try {
            const response = await axios.post(`http://127.0.0.1:5000/${urlName}`, formData);
            if (response.data.message === "success")
                setTimestamps(response.data.timestamps);
        } catch (error) {
            console.error(error)
        }
    }

    useEffect(() => {
        if (id === "video")
            file1 && storeImage("detect");
        else if (id === "realtime")
            file1 && storeImage("realtime");
        else
            file1 && storeImage("database-read");

    }, [file1, id]);

    id === "video" && useEffect(() => {
        const storeVideo = async () => {
            const formData = new FormData();
            formData.append('videoFile', file2);
            try {
                const response = await axios.post(`http://127.0.0.1:5000/process_video`, formData);
                console.log(response);
            } catch (error) {
                console.error(error)
            }
        }
        file2 && storeVideo();
    }, [file2])

    id === "realtime" && useEffect(() => {
        const storeVideo = async () => {
            const formData = new FormData();
            formData.append('image', file2);
            try {
                const response = await axios.post(`http://127.0.0.1:5000/realtime-download`, formData);
                if (response.data.message === "success") {
                    setTimestamps(response.data.timestamps);
                    setFrames(response.data.frames);
                }
            } catch (error) {
                console.error(error)
            }
        }
        file2 && storeVideo();
    }, [file2]);

    useEffect(() => {
        socket.on('face_detected', (data) => {
            const { timestamps } = data;
            setTimestamps(prev => [...prev, Date(timestamps)]);
        });
        socket.on('face_detected_frame', (data) => {
            const { frameName } = data;
            setFrames(prev => [...prev, frameName])
        })
    }, [socket]);

    return (
        <aside id={id} className='my-28 flex flex-col items-center justify-center'>
            <h1 className='text-5xl m-20 font-["Viga"] text-slate-700'>{name}</h1>
            <div className='w-full flex'>
                <div className={`w-1/3 p-10 bg-[#8381FD] flex ${id === "video" ? "flex-col-reverse" : "flex-col"} flex-col items-center justify-center`}>
                    <input onChange={(e) => setFile1(e.target.files[0])} className='hidden' id={`${id === "video" ? "fbtn1" : (id === "realtime" ? "rbtn1" : "dbtn1")}`} type="file" />
                    {!(id === "database") && <label htmlFor={`${id === "video" ? "fbtn1" : (id === "realtime" ? "rbtn1" : "dbtn2")}`} className='cursor-pointer p-4 bg-[#4A51ED] text-white text-2xl rounded-xl my-8'>Upload Image</label>}
                    <input onChange={(e) => setFile2(e.target.files[0])} className='hidden' id={`${id === "video" ? "fbtn2" : (id === "realtime" ? "rbtn2" : "dbtn2")}`} type="file" />
                    <label htmlFor={`${id === "video" ? "fbtn2" : (id === "realtime" ? "rbtn2" : "dbtn1")}`} className={`flex items-center cursor-pointer p-4 bg-[#4A51ED] text-white text-2xl rounded-xl my-8`}><img src="./assets/svgs/tick.gif" className={`${id === "realtime" && file2 != null && frames.length !== 0 ? "" : "hidden"} w-10 h-10 mr-1`} alt="" />{id === "realtime" ? "Download" : (id === "video" ? "Upload Video" : "Upload Image")}</label>
                </div>
                <div className='w-1/3 p-14 bg-[#5F64E6] flex items-center justify-center'>
                    <img src="/assets/svgs/faceTracking.svg" alt="" />
                </div>
                <div className='w-1/3 p-10 bg-[#2E3E8A] text-slate-300 flex flex-col items-center'>
                    <h3 className='text-3xl mb-2 text-white'>Timestamp</h3>
                    <div className='h-80 px-3 scrollbar'>
                        {(id === "realtime" && file2) || file1 !== null ? (timestamps.length !== 0 ? timestamps.map((timestamp, index) => (<p key={index}>{id === "video" ? `Face Detected at ${timestamp} seconds` : timestamp}</p>)) : "No Face Detected!") : "No Image Selected!"}
                    </div>
                </div>
            </div>
            <div className={`mt-4 p-2 flex overflow-x-auto`}>
                {
                    id === "realtime" && (frames.length !== 0 && frames.map(frame => {
                        console.log(frame)
                        return <img className='h-36 w-36 rounded-lg mx-2' src={'/assets/realtimeFrames/' + frame} />
                    }))
                }
            </div>
        </aside>
    )
}

export default FaceTracking