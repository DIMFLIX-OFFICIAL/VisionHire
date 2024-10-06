import axios from 'axios';
import { logout } from "@/modules/auth";

const api = axios.create();

api.interceptors.response.use(
	response => {
	  return response;
	},
	error => {
		if (error.response && error.response.status === 401) {
			console.log("Unauthorized api!");
			logout();
		}
		return Promise.reject(error);
	}
);

export async function getAccountInfo() {
	return api.post("/api/protected/get_my_account_info")
		.then(response => {
			return JSON.parse(response.data)
		})
		.catch(e => { return null })
}

export async function create_task(title_todo, description_todo, task_receiver) {
    console.log("вызвал")
   
        try {
            const taskData = {
                title: title_todo,
                description: description_todo,
                task_receiver: task_receiver,
            };

            let response = await api.post("/api/protected/create_task", taskData);
            console.log("Task created successfully:", response.data);
        } catch (error) {
            console.error("Error creating task:", error.response ? error.response.data : error.message);
            alert("Ошибка при создании задачи: " + (error.response ? error.response.data.detail : error.message));
        }
    }
       



export async function getSubs(){
    try{
        let response = await api.post("/api/protected/get_subs")
        return JSON.parse(response.data)

    }catch(error){
        console.log(error)
        
    }
}


export async function getTasks(){
    try{
        let response = await api.post("/api/protected/get_tasks")
        console.log(response.data)
        return response.data

    }catch(error){
        console.log(error)
        
    }


}

export async function getMetrNewCandidates(date_from, date_to) {

        try {
            const data = {
                date_from: date_from,
                date_to: date_to,
            };

            let response = await api.post("/api/protected/get_met_new_candidates", data);
            console.log("Met get successfully:", response.data);
        } catch (error) {
            console.error("Met get successfully:", error.response ? error.response.data : error.message);

        }
    }