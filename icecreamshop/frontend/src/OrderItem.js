import { useState } from 'react'


function OrderItem({icecream_tubs, flavors}) {
	const [selectedIceCreamTub, setSelectedIceCreamTub] = useState('')
	const [scoopsRequested, setScoopsRequested] = useState(1)

  function getFlavorByName(name, flavors) {
    return flavors.find(flavor => flavor.name === name);
  }

  console.log("selectedIceCreamTub", selectedIceCreamTub)

	const handleIceCreamTubChange = event => {
    setSelectedIceCreamTub(event.target.value)

  }

	const handleScoopsRequestedChange = event => {
    setScoopsRequested(Number(event.target.value));
  }

  return (
    <div className="form-container">
      <label className="label" htmlFor="flavor-select">Select an ice cream:</label>
      <select
        className="select"
        id="flavor-select"
        value={selectedIceCreamTub}
        onChange={handleIceCreamTubChange}
      >
        <option value="">--Select an ice cream--</option>
        {icecream_tubs.map((iceCreamTub) => (
          <option key={iceCreamTub.id} value={iceCreamTub.flavor_name}>
            {`${iceCreamTub.flavor_name} - ${iceCreamTub.scoops_available} scoops left`}
          </option>
        ))}
      </select>
      <br />
      <label className="label" htmlFor="num-scoops-select">Number of scoops:</label>
      <input
        className="input"
        id="num-scoops-input"
        type="number"
        min="1"
        value={scoopsRequested}
        onChange={handleScoopsRequestedChange}
      />
      {selectedIceCreamTub && <img src={getFlavorByName(selectedIceCreamTub, flavors).photo} alt={selectedIceCreamTub.flavor_name} />}
    </div>
  );
}

export default OrderItem;