export const InputText = ({handleSubmit, button_name}) => {
    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input type="text" name="url" placeholder="URL"/>
                <input type="submit" value={button_name}/> 
            </form>
        </div>
    );
}