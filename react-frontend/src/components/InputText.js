export const InputText = ({handleSubmit}) => {
    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input type="text" name="url" placeholder="URL"/>
                <input type="submit" value="submit"/> 
            </form>
        </div>
    );
}