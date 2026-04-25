
import { useState } from 'react';
import axios from 'axios';
const api = axios.create({baseURL:'http://localhost:8000'})
function Queries(){
    const [question,setQuestion]=useState('');
    const [answer,setAnswer]= useState('');
    const [urll,setUrl]=useState('');
    const [urlres,setUrlres]= useState('');
    const handleSubmit= async (e) =>
    {
        e.preventDefault();
        console.log("your question",question);
        const response= await api.post('/chat',{message:question});
        setAnswer(response.data.answer);
        console.log("Answer",answer)
    }

    const handleURLSubmit= async (e) =>
    {
        e.preventDefault();
        console.log("your source link",urll);
        const response_urll= await api.post('/load_doc',{mes:urll});
        setUrlres(response_urll.data);
        console.log("urlresponse",urlres)
    }
    return(
    <div>
        <form>
           

            <input type="text" value ={urll}  pattern="https?://.*" onChange={(e)=> setUrl(e.target.value)} />
            <button type ="submit" onClick={handleURLSubmit}>Submit your url</button>
        </form>
        
         <p>{urlres ? JSON.stringify(urlres) : "No data yet"}</p>

          <input type="text" value ={question} onChange={(e)=> setQuestion(e.target.value)} />
            <button type ="submit" onClick={handleSubmit}>Submit</button>

    <div>
            <p>Answer</p>
            <p>{answer}</p>
        </div>
    </div>
    );
}
export default Queries;