export const InputText = ({handleSubmit, button_name}) => {
    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input
                    className="w-64 py-2 px-2 border border-gray-200 rounded-l focus:outline-none focus:ring-blue-400"
                    type="text"
                    name="url"
                    placeholder="URL"
                />
                <input 
                    className="font-bold bg-blue-900 hover:bg-blue-800 text-white py-2 px-3 rounded"
                    type="submit"
                    value={button_name}
                /> 
            </form>
        </div>
    );
}