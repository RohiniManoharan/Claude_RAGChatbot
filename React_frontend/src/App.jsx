import { useState } from 'react'

import Queries from './Queries'

function App() {
  const [count, setCount] = useState(0)
return(
  <div>
    <div>Hi there!</div>
    <Queries/>
    
    </div>
)
}
export default App
