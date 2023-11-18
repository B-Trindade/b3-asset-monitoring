import React from 'react'
import CustomNavbar from '../components/CustomNavbar'
import UserTickersTable from '../components/UserTickersTable'

const HomePage = () => {
  return (
    <div>
      <CustomNavbar/>
      <UserTickersTable />
    </div>
  )
}

export default HomePage