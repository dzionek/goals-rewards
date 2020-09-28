import React from 'react'
import {render} from '@testing-library/react'

import Test from "../components/Test"

describe("<Test/>", () => {
    it("renders Hello World", () => {
        const {getByText} = render(<Test/>)
        getByText("Hello World")
    })
})