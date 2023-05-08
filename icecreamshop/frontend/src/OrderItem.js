import { useState } from 'react'


function OrderItem({icecream_tubs}) {
	const [selectedIceCreamTub, setSelectedIceCreamTub] = useState('')
	const [scoopsRequested, setScoopsRequested] = useState(1)

	const handleIceCreamTubChange = event => {
    setSelectedIceCreamTub(event.target.value);
  }

	const handleScoopsRequestedChange = event => {
    setScoopsRequested(Number(event.target.value));
  }

  return (
    <div>
        <label htmlFor="flavor-select">Select an ice cream:</label>
            <select id="flavor-select" value={selectedIceCreamTub} onChange={handleIceCreamTubChange}>
							<option value="">--Select an ice cream--</option>
							{icecream_tubs.map((iceCreamTub) => (
								<option key={iceCreamTub.id} value={iceCreamTub.flavor}>
									{iceCreamTub.flavor_name}
								</option>
							))}
        		</select>
        <br />
        <label htmlFor="num-scoops-select">Number of scoops:</label>
            <select id="num-scoops-select" value={scoopsRequested} onChange={handleScoopsRequestedChange}>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
        </select>
    </div>
  );
}

export default OrderItem;