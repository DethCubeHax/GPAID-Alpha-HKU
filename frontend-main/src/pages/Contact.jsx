import "./Contact.css"
import { FaGithub } from "react-icons/fa";
import { EmailIcon } from "@chakra-ui/icons";

const ContactPage = () => {
    return(
        <div>
            <div className="roundBox">
                <div className="titlec">
                    <div style={{textAlign:"center"}}>This website was developed by the blood, sweat and tears of</div>
                </div>
                <div style={{display:"flex", minWidth:"100%"}}>
                <div style={{flex:1, textAlign:"left"}}>
                        <div style={{display:"flex", minWidth:"100%"}}>
                            <div style={{flex:1}}>
                                <div style={{padding:"50px"}}>
                                    <img src="https://avatars.githubusercontent.com/u/114172779?v=4" />
                                </div>
                            </div>
                            <div style={{flex:1}}>
                                <div style={{paddingTop:"90px"}}>
                                    <div className="devNamec">Wasif Latif Hussain</div>
                                    <a target="_blank" href="https://github.com/wasifcoding/">
                                        <div style={{display:"flex"}}>
                                            <FaGithub></FaGithub>
                                            <div style={{paddingLeft:"15px", position:"relative", bottom:"4px"}}>
                                                wasifcoding
                                            </div>
                                        </div>
                                    </a>
                                    <a target="_blank" href="">
                                        <div style={{display:"flex"}}>
                                            <EmailIcon></EmailIcon>
                                            <div style={{paddingLeft:"15px", position:"relative", bottom:"4px"}}>
                                                md.wasiflatif9859@gmail.com
                                            </div>
                                        </div>
                                    </a>
                                </div>
                            </div>
                            
                        </div>
                    </div>
                    <div style={{flex:1, textAlign:"left"}}>
                        <div style={{display:"flex", minWidth:"100%"}}>
                            <div style={{flex:1}}>
                                <div style={{padding:"50px"}}>
                                    <img src="https://avatars.githubusercontent.com/u/57101067?v=4"/>
                                </div>
                                
                            </div>
                            <div style={{flex:1}}>
                                <div style={{paddingTop:"90px"}}>
                                    <div className="devNamec">Nafis ul Islam</div>
                                    <a target="_blank" href="https://www.github.com/DethCubeHax">
                                        <div style={{display:"flex"}}>
                                            <FaGithub></FaGithub>
                                            <div style={{paddingLeft:"15px", position:"relative", bottom:"4px"}}>
                                                DethCubeHax
                                            </div>
                                        </div>
                                    </a>
                                    <a target="_blank" href="">
                                        <div style={{display:"flex"}}>
                                            <EmailIcon></EmailIcon>
                                            <div style={{paddingLeft:"15px", position:"relative", bottom:"4px"}}>
                                                nafisulislam2k2@gmail.com
                                            </div>
                                        </div>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    )
}

export default ContactPage;