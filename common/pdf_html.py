pdf_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Details Tables</title>
    <style>
      * {
        font-family: Verdana, Geneva, Tahoma, sans-serif;
      }
      h2 {
        text-align: center;
      }
      table {
        margin-left: 25%;
        margin-right: 25%;
        border-collapse: collapse;
        width: 50%;
        border: 0.5px solid black;
      }
      th,
      td {
        text-align: center;
        padding: 8px;
        font-size: 14px;
		text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
  max-width: 200px;
      }

      tr:nth-child(even) {
        background-color: #f2f2f2;
      }

      th {
        background-color: slategrey;
        color: white;
      }

    </style>
  </head>

  <body>
    <!-- First Table: Memo Details -->
    <h2>Memo Details</h2>
    <table>
      <tbody>
        <tr>
          <th style="width: 200px;">Name</th>
          <td style="text-align: left">{name}</td>
        </tr>
        <tr>
          <th>Address</th>
          <td style="text-align: left">
            {address}
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Second Table: Traffic Violation Details -->
    <h2>Traffic Violation Details</h2>
    <table>
      <tbody>
        <tr>
          <th>Vehicle Reg. No.</th>
          <td>{reg_no}</td>
          <th>Vehicle Maker/Model</th>
          <td>{vehicle_maker} {vehicle_model}</td>
        </tr>
        <tr>
          <th>Challan No.</th>
          <td>948392843</td>
          <th>Vehicle Type</th>
          <td>{vehicle_type}</td>
        </tr>
        <tr>
          <th>Date of Violation</th>
          <td>{date_of_violation}</td>
          <th>Mobile No.</th>
          <td>{mobile_number}</td>
        </tr>
      </tbody>
    </table>
	<div style="width: 100%; display: flex; justify-content: center">
        <img src={img_url} style="width: 600px; height: 400px;">
    </div>
  </body>
</html>
"""