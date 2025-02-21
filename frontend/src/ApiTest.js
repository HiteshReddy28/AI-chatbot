import { useState } from "react";

function Test(){

    const[data, setData] = useState("");
    const func = async()=> {
    try{
        const response = await fetch("http://127.0.0.1:8000");
        const appdata = await response.json();
        setData(appdata.message);
    }
    catch(error){
console.log("your code has error");
    }
    }
    return(
        <>
        <h1>React-Dom</h1>
        <button onClick={func}> Click me!</button>
        <p>{data}</p>
        
        </>
    )
}
export default Test;