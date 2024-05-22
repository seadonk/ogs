import logo from './logo.svg';
import './App.css';
import {useEffect, useState} from "react";

const hostType = 's3';
const hosts = {
    local: process.env.PUBLIC_URL,
    s3: 'https://60048-ogs.s3.us-east-2.amazonaws.com'
}
const host = hosts.s3
const dataUrl = `${host}/output.json`


function Header({setSearchValue}) {
    return (
        <header className="header">
            <input
                type="text"
                placeholder="Search meetings by title/date"
                onChange={e => setSearchValue(e.target.value)}
            />
        </header>
    );
}

function Meeting({meeting}) {
    const {meeting: description, minutes_id, agenda, video, minutes} = meeting;
    return (
        <div className='meeting-item'>
            <div>{description}</div>
            <div className='item-link'>
                <div>{agenda && <a href={agenda}>agenda</a>}</div>
                <div>{video && <a href={video}>video</a>}</div>
                <div>{minutes && <a href={`${host}/minutes/${minutes_id}.pdf`}>minutes</a>}</div>
            </div>
        </div>
    );
}

function Meetings() {
    const [meetings, setMeetings] = useState([]);
    const [searchValue, setSearchValue] = useState('');
    useEffect(() => {
        fetch(dataUrl)
            .then(response => response.json())
            .then(data => setMeetings(data))
            .catch(error => console.error('Error:', error));
    }, []);

    const filteredMeetings = meetings.filter(meeting =>
        meeting.meeting.toLowerCase().includes(searchValue.toLowerCase())
    );

    return (
        <div className='meetings'>
            <Header setSearchValue={setSearchValue}/>
            {filteredMeetings.map(meeting => (
                <Meeting key={meeting.meeting_number} meeting={meeting}/>
            ))}
        </div>
    );
}


function App() {
    return (
        <div className="App">
            <Meetings/>
        </div>
    );
}

export default App;
